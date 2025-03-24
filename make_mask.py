# 这有个问题，好像没把背景网格的尺寸加进去
import numpy as np
import trimesh  # 用于读取 STL 文件
import pickle

# 定义计算域大小
nx, ny, nz = 540, 240, 1  # 二维模型时 nz=1
Lx, Ly, Lz = 1.0, 1.0, 1.0  # 背景网格的物理尺寸
dx, dy, dz = Lx / nx, Ly / ny, Lz / nz  # 网格间距

# 加载 STL 文件
mesh = trimesh.load_mesh('D:/tutorial/case1/constant/triSurface/wall.stl')

# 初始化掩码数组
mask = np.zeros((nx, ny, nz), dtype=int)

for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            # 计算网格点的物理坐标
            x = i * dx
            y = j * dy
            z = k * dz
            point = np.array([x, y, z])
            # 判断点是否在几何体内
            if mesh.contains([point]):
                mask[i, j, k] = 1  # 标记为几何体区域

# 保存掩码数据到 pkl 文件
with open('mask2.pkl', 'wb') as f:
    pickle.dump(mask, f)

print("掩码数据已生成并保存为 mask2.pkl")
