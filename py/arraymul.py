import numpy as np
import matplotlib.pyplot as plt

# 1. 定义长方形的 4 个原始顶点 (闭合曲线，所以重复第一个点)
x_orig = np.array([0, 1, 1, 0, 0])
y_orig = np.array([0, 0, 3, 3, 0])
orig_coords = np.vstack((x_orig, y_orig)) # 组合成 2x5 的矩阵

# 2. 定义空间变换矩阵 A
A = np.array([[2, 1],
              [1, 2]])

# 3. 核心：通过矩阵乘法，一瞬间完成空间变换！
trans_coords = A @ orig_coords # 结果是 2x5 的新坐标矩阵
x_trans = trans_coords[0, :]
y_trans = trans_coords[1, :]

# 4. 开始画图：创建左右两个对比画布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# ---- 左画布：变换前的标准长方形 ----
ax1.plot(x_orig, y_orig, color='#2ecc71', linewidth=3, label='Original Rectangle')
ax1.fill(x_orig, y_orig, color='#2ecc71', alpha=0.3)
ax1.set_title("Before Transformation\n(Area = 1 × 3 = 3)", fontsize=12, fontweight='bold')

# ---- 右画布：变换后的倾斜平行四边形 ----
ax2.plot(x_trans, y_trans, color='#f39c12', linewidth=3, label='Transformed Shape')
ax2.fill(x_trans, y_trans, color='#f39c12', alpha=0.3)
ax2.set_title("After Transformation\n(Area = 3 × det(A) = 9)", fontsize=12, fontweight='bold')

# ---- 统一美化坐标轴（方便肉眼对比刻度变化） ----
for ax in [ax1, ax2]:
    ax.axhline(0, color='black',linewidth=1.2) # 画出 X 轴
    ax.axvline(0, color='black',linewidth=1.2) # 画出 Y 轴
    ax.grid(True, linestyle='--', alpha=0.6)     # 加上虚线网格
    ax.set_xlim(-1, 7)                           # 统一横坐标范围
    ax.set_ylim(-1, 9)                           # 统一纵坐标范围
    ax.set_aspect('equal')                       # 保持 1:1 的真实几何比例
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')

# 5. 优雅展现
plt.tight_layout()
plt.show()

