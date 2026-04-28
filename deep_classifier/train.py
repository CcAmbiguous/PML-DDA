"""
train.py
10 折交叉验证训练主入口。
运行方式：python train.py
"""
import random
import os
import numpy as np
import torch
import torch.optim as optim

import config
from data_loader import load_fold
from model import MultiLabelClassifier, NoisyBCELoss
from metrics import (
    HammingLoss,
    OneError,
    Coverage,
    RankingLoss,
    AveragePrecision,
)


# ─────────────────────────────────────────
#  设备选择
# ─────────────────────────────────────────
def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # 保证 cudnn 的确定性（可能略微降低速度）
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark     = False

def get_device():
    if config.DEVICE == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(config.DEVICE)

# ─────────────────────────────────────────
#  单折训练
# ─────────────────────────────────────────

def train_one_fold(fold: int, device: torch.device):
    """
    训练第 fold 折，返回测试集上的 5 个评价指标。
    """
    print(f"\n{'='*50}")
    print(f"  Fold {fold:>2d} / 10")
    print(f"{'='*50}")

    # set_seed(config.SEED + fold)   

    # ── 加载数据 ────────────────────────────
    train_loader, test_loader, input_dim, output_dim = load_fold(
        data_dir     = config.DATA_DIR,
        dataset_name = config.DATASET_NAME,
        fold         = fold,
        batch_size   = config.BATCH_SIZE,
    )
    print(f"  input_dim={input_dim}, output_dim={output_dim}, "
          f"train_batches={len(train_loader)}, test_batches={len(test_loader)}")

    # ── 模型、损失、优化器 ──────────────────
    model = MultiLabelClassifier(
        input_dim   = input_dim,
        hidden_dims = config.HIDDEN_DIMS,
        output_dim  = output_dim,
    ).to(device)

    criterion = NoisyBCELoss()
    optimizer = optim.Adam(
        model.parameters(),
        lr           = config.LR,
        weight_decay = config.WEIGHT_DECAY,
    )

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=config.T_MAX, eta_min=config.ETA_MIN
)
    
    
# ── 训练循环 ────────────────────────────
    os.makedirs(config.SAVE_DIR, exist_ok=True)
    save_path = os.path.join(
        config.SAVE_DIR,
        f"{config.DATASET_NAME}_cv{fold}.pth"
    )

    best_loss  = float('inf')
    no_improve = 0

    for epoch in range(1, config.EPOCHS + 1):
        model.train()
        epoch_loss = 0.0
        for X_batch, Y_batch, YN_batch in train_loader:
            X_batch  = X_batch.to(device)
            Y_batch  = Y_batch.to(device)
            YN_batch = YN_batch.to(device)

            optimizer.zero_grad()
            y_pred = model(X_batch)
            loss   = criterion(y_pred, Y_batch, YN_batch)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item() * X_batch.size(0)

        scheduler.step()

        avg_loss = epoch_loss / len(train_loader.dataset)
        if epoch % 10 == 0 or epoch == 1:
            current_lr = scheduler.get_last_lr()[0]
            print(f"  Epoch [{epoch:>4d}/{config.EPOCHS}]  Loss: {avg_loss:.6f}  LR: {current_lr:.2e}")

        # ── 早停判断 ────────────────────────
        if avg_loss < best_loss - config.MIN_DELTA:
            best_loss  = avg_loss
            no_improve = 0
            torch.save(model.state_dict(), save_path)  # 保存当前最优
        else:
            no_improve += 1
            if no_improve >= config.PATIENCE:
                print(f"  早停触发：Epoch {epoch}，最优 Loss {best_loss:.6f}")
                break

    # 加载最优模型再去测试
    model.load_state_dict(torch.load(save_path))
    print(f"  已加载最优模型（Loss: {best_loss:.6f}）")

    # ── 测试集评估 ──────────────────────────
    metrics = evaluate(model, test_loader, device)
    return metrics


# ─────────────────────────────────────────
#  评估函数
# ─────────────────────────────────────────

def evaluate(model, test_loader, device: torch.device):
    """
    在 test_loader 上评估 5 个多标签指标。
    返回 dict：{metric_name: float}
    """
    model.eval()
    all_scores = []
    all_labels = []

    with torch.no_grad():
        for X_batch, Y_batch in test_loader:
            X_batch = X_batch.to(device)
            scores  = model(X_batch)          # sigmoid 输出，即预测概率
            all_scores.append(scores.cpu())
            all_labels.append(Y_batch.cpu())

    pred_scores  = torch.cat(all_scores, dim=0)   # (M, Q)
    target_labels = torch.cat(all_labels, dim=0)  # (M, Q)

    # 二值化用于 HammingLoss
    pred_labels = (pred_scores >= config.THRESHOLD).float()

    results = {
        "HammingLoss"      : HammingLoss(pred_labels, target_labels),
        "OneError"         : OneError(pred_scores, target_labels),
        "Coverage"         : Coverage(pred_scores, target_labels),
        "RankingLoss"      : RankingLoss(pred_scores, target_labels),
        "AveragePrecision" : AveragePrecision(pred_scores, target_labels),
    }
    return results


# ─────────────────────────────────────────
#  主程序
# ─────────────────────────────────────────

def main():
    set_seed(config.SEED) 
    device = get_device()
    print(f"\n使用设备: {device}")
    print(f"数据集: {config.DATASET_NAME}")
    print(f"隐藏层维度: {config.HIDDEN_DIMS}")
    print(f"Epochs={config.EPOCHS}, BatchSize={config.BATCH_SIZE}, LR={config.LR}")

    metric_names = [
        "HammingLoss",
        "OneError",
        "Coverage",
        "RankingLoss",
        "AveragePrecision",
    ]

    # 收集 10 折结果
    all_results = {name: [] for name in metric_names}

    for fold in range(1, 11):
        metrics = train_one_fold(fold, device)

        print(f"\n  [Fold {fold}] 测试指标:")
        for name in metric_names:
            val = metrics[name]
            all_results[name].append(val)
            print(f"    {name:<20s}: {val:.6f}")

    # ── 打印汇总结果 ────────────────────────
    print(f"\n{'='*60}")
    print(f"  10 折汇总结果（{config.DATASET_NAME}）")
    print(f"{'='*60}")
    print(f"  {'Metric':<22s}  {'Mean':>10s}  {'Std':>10s}")
    print(f"  {'-'*46}")
    for name in metric_names:
        vals = np.array(all_results[name])
        mean = vals.mean()
        std  = vals.std()
        print(f"  {name:<22s}  {mean:>10.6f}  {std:>10.6f}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
