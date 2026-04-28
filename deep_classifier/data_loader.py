"""
data_loader.py
加载单个 .mat 文件，返回 PyTorch Tensor 及 DataLoader。
mat 文件内包含：X_train, X_test, Y_train, Y_test, Y_noise
"""

import os
import scipy.io
import torch
from torch.utils.data import Dataset, DataLoader


# ─────────────────────────────────────────
#  Dataset
# ─────────────────────────────────────────

class MultiLabelDataset(Dataset):
    """训练集：同时持有 Y_train 和 Y_noise（用于自定义损失）"""

    def __init__(self, X: torch.Tensor, Y: torch.Tensor, Y_noise: torch.Tensor):
        assert X.shape[0] == Y.shape[0] == Y_noise.shape[0], \
            "X / Y / Y_noise 样本数不一致"
        self.X       = X
        self.Y       = Y
        self.Y_noise = Y_noise

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx], self.Y_noise[idx]


class TestDataset(Dataset):
    """测试集：只需要 X 和 Y"""

    def __init__(self, X: torch.Tensor, Y: torch.Tensor):
        assert X.shape[0] == Y.shape[0]
        self.X = X
        self.Y = Y

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]


# ─────────────────────────────────────────
#  加载函数
# ─────────────────────────────────────────

def load_fold(data_dir: str, dataset_name: str, fold: int, batch_size: int = 64):
    """
    加载第 fold 折数据（fold 从 1 开始）。

    Parameters
    ----------
    data_dir     : mat 文件所在目录
    dataset_name : 数据集名称前缀，如 'emotions'
    fold         : 1 ~ 10
    batch_size   : DataLoader batch size

    Returns
    -------
    train_loader : DataLoader  （X_train, Y_train, Y_noise）
    test_loader  : DataLoader  （X_test,  Y_test）
    input_dim    : int
    output_dim   : int
    """
    filename = f"{dataset_name}_cv{fold}.mat"
    filepath = os.path.join(data_dir, filename)

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"找不到数据文件：{filepath}")

    mat = scipy.io.loadmat(filepath)

    def to_tensor(key):
        arr = mat[key]
        return torch.tensor(arr, dtype=torch.float32)

    X_train = to_tensor("X_train")
    X_test  = to_tensor("X_test")
    Y_train = to_tensor("Y_train")
    Y_test  = to_tensor("Y_test")
    Y_noise = to_tensor("Y_noise")

    # mean = X_train.mean(dim=0, keepdim=True)
    # std  = X_train.std(dim=0, keepdim=True) + 1e-8
    # X_train = (X_train - mean) / std
    # X_test  = (X_test  - mean) / std   

    train_dataset = MultiLabelDataset(X_train, Y_train, Y_noise)
    test_dataset  = TestDataset(X_test, Y_test)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader  = DataLoader(test_dataset,  batch_size=batch_size, shuffle=False)

    input_dim  = X_train.shape[1]
    output_dim = Y_train.shape[1]

    return train_loader, test_loader, input_dim, output_dim
