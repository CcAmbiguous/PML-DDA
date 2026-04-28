# ─────────────────────────────────────────
#  全局配置
# ─────────────────────────────────────────

# 数据集名称前缀，对应文件 {DATASET_NAME}_cv1.mat ~ {DATASET_NAME}_cv10.mat
DATASET_NAME = "emotions3"

# mat 文件所在目录（相对或绝对路径）
DATA_DIR = "./data"

# 模型保存目录
SAVE_DIR = "./saved_models"

# ── 模型结构 ──────────────────────────────
# 隐藏层维度列表，可任意加深/改宽
# HIDDEN_DIMS = [64, 32] #emotions,image
# HIDDEN_DIMS = [512, 512] #birds
# HIDDEN_DIMS = [512, 256] #其他数据集

HIDDEN_DIMS = [64, 32] 

# ── 训练超参数 ────────────────────────────
EPOCHS     = 400
BATCH_SIZE = 64
LR         = 1e-3          # 学习率
WEIGHT_DECAY = 1e-5        # L2 正则


T_MAX = 400   # 余弦退火周期
ETA_MIN = 1e-7  # 学习率下界
# 标签二值化阈值（用于 HammingLoss）
THRESHOLD = 0.5

# 设备：'cuda' / 'cpu' / 'auto'
DEVICE = "auto"
SEED = 42

# 早停
PATIENCE  = 20       # 连续多少个 epoch 没改善就停
MIN_DELTA = 1e-4     # 改善幅度低于此值也算没改善