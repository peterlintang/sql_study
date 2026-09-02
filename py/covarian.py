import torch

# 1. 原始数据：3个房子（行），每个房子有[面积, 价格]2个特征（列）
# 此时数据远离原点
data = torch.tensor([[120.0, 400.0],
                     [150.0, 550.0],
                     [90.0,  250.0]])

# ──── 第一步：去中心化（零均值化） ────
mean = torch.mean(data, dim=0) # 算出各列的平均值
data_centered = data - mean    # 减去均值，把重心拉回 (0,0)

# ──── 第二步：计算协方差矩阵 ────
# 公式：(X^T * X) / (N - 1)
N = data_centered.size(0)
covariance_matrix = (data_centered.T @ data_centered) / (N - 1)
print("转换出的协方差矩阵（空间变换魔术师）:")
print(covariance_matrix)

# ──── 第三步：榨取特征值与特征向量 ────
# 使用 torch.linalg.eigh（专门用于对称矩阵，比 eig 更快更稳定）
eigenvalues, eigenvectors = torch.linalg.eigh(covariance_matrix)

# 注意：PyTorch 默认输出的特征值是从小到大排列的
# 我们通常把它倒序，改成从大到小，方便挑出“最重要的主成分”
eigenvalues = torch.flip(eigenvalues, dims=[0])
eigenvectors = torch.flip(eigenvectors, dims=[1])

print("\n【大功告成】")
print("1. 挖掘出的特征值（能量/信息量大小）:")
print(eigenvalues) 
print("2. 挖掘出的特征向量（骨架主轴方向，按列看）:")
print(eigenvectors)

