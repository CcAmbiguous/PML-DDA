"""
model.py
多标签分类器：Linear→Tanh → Linear→Tanh → Linear→Sigmoid
以及改进的 BCE 损失函数。
"""

import torch
import torch.nn as nn


# ─────────────────────────────────────────
#  网络结构
# ─────────────────────────────────────────

class MultiLabelClassifier(nn.Module):
    """
    前向公式：Y_predict = sigmoid( tanh( tanh(X) ) )

    结构：
        Input → [Linear → Tanh] x len(hidden_dims) → Linear → Sigmoid → Output

    Parameters
    ----------
    input_dim   : 输入特征维度
    hidden_dims : 隐藏层维度列表，如 [256, 128]
    output_dim  : 标签数量
    """

    def __init__(self, input_dim: int, hidden_dims: list, output_dim: int):
        super().__init__()

        layers = []
        prev_dim = input_dim

        # 隐藏层：Linear + Tanh
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.Tanh())
            prev_dim = h_dim

        # 输出层：Linear + Sigmoid
        layers.append(nn.Linear(prev_dim, output_dim))
        layers.append(nn.Sigmoid())

        self.net = nn.Sequential(*layers)

        # 权重初始化（xavier 对 tanh 友好）
        self._init_weights()

    def _init_weights(self):
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


# ─────────────────────────────────────────
#  改进的 BCE 损失
# ─────────────────────────────────────────

class NoisyBCELoss(nn.Module):
    """
    改进 BCE 损失，负样本部分使用 Y_noise：

        loss = -1/N * Σ [ Y_train * log(Y_pred)
                         + (1 - Y_noise) * log(1 - Y_pred) ]

    Parameters
    ----------
    eps : 数值稳定项，防止 log(0)
    """

    def __init__(self, eps: float = 1e-7):
        super().__init__()
        self.eps = eps

    def forward(
        self,
        y_pred:  torch.Tensor,   # (N, Q) sigmoid 输出，范围 (0, 1)
        y_train:  torch.Tensor,   # (N, Q) 真实标签 0/1
        y_noise: torch.Tensor,   # (N, Q) 噪声标签 0/1
    ) -> torch.Tensor:

        y_pred  = y_pred.clamp(self.eps, 1.0 - self.eps)

        pos_term = y_train  * torch.log(y_pred)
        neg_term = (1.0 - y_noise) * torch.log(1.0 - y_pred)

        loss = -(pos_term + neg_term).mean()
        return loss
