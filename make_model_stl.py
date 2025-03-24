# 生成的stl模型，需要有厚度才能让snappyhexmesh识别，因为snsppyhexmesh是对于三维的才能使用
import numpy as np
import stl
from stl import mesh

# 设置边长
side_length = 10  # 10mm
scale = 0.001  # 从 mm 转换到 m
thickness = 1 * scale  # 厚度为 1mm

# 计算正三角形的顶点（让原点在中心）
height = (np.sqrt(3) / 2) * side_length  # 计算高
vertices = np.array([
    [-side_length / 2, -height / 3, 0],  # 顶点 1
    [side_length / 2, -height / 3, 0],   # 顶点 2
    [0, 2 * height / 3, 0]              # 顶点 3
]) * scale  # 这里缩小 1000 倍，使 STL 适用于 OpenFOAM（假设 STL 以 m 计）

# 复制顶点并增加厚度（Z 方向）
vertices_with_thickness = np.vstack([
    vertices,  # 原始顶点（底部）
    vertices + [0, 0, thickness]  # 复制并平移顶点（顶部）
])

# 定义面（三角形和侧面）
faces = [
    # 底部三角形
    [0, 1, 2],
    # 顶部三角形
    [3, 4, 5],
    # 侧面 1
    [0, 1, 4],
    [0, 4, 3],
    # 侧面 2
    [1, 2, 5],
    [1, 5, 4],
    # 侧面 3
    [2, 0, 3],
    [2, 3, 5]
]

# 创建 STL mesh
triangle_with_thickness = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        triangle_with_thickness.vectors[i][j] = vertices_with_thickness[f[j]]

# 保存 STL 文件
triangle_with_thickness.save("triangle_with_thickness_mm.stl")

print("已生成 triangle_with_thickness_mm.stl，边长 10mm，厚度 1mm，原点在中心")
