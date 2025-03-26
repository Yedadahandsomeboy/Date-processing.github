# 生成的stl模型，需要有厚度才能让snappyhexmesh识别，因为snsppyhexmesh是对于三维的才能使用
import numpy as np
import stl
from stl import mesh
import random

def generate_random_triangle():
    while True:
        # 生成符合面积要求的三角形
        x1, y1 = random.uniform(-5, 0), random.uniform(0, 5)  # 第二象限
        x2, y2 = random.uniform(0, 5), random.uniform(-5, 0)  # 第四象限
        x3, y3 = random.uniform(-5, 0), random.uniform(-5, 0) # 第三象限
        
        area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
        
        if 25 <= area <= 50:
            return np.array([[x1, y1, 0], [x2, y2, 0], [x3, y3, 0]])

def create_stl(triangle_vertices, index, thickness=1):
    # 复制并增加厚度
    vertices_with_thickness = np.vstack([
        triangle_vertices,
        triangle_vertices + [0, 0, thickness]  # 平移 Z 方向增加厚度
    ])

    print(f"模型 {index} 顶点坐标:\n", vertices_with_thickness)  # **检查顶点是否有厚度**

    # 定义面
    faces = [
        [0, 1, 2],  # 底部三角形
        [3, 4, 5],  # 顶部三角形
        [0, 1, 4], [0, 4, 3],  # 侧面1
        [1, 2, 5], [1, 5, 4],  # 侧面2
        [2, 0, 3], [2, 3, 5]   # 侧面3
    ]

    # 创建 STL mesh
    triangle_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            triangle_mesh.vectors[i][j] = vertices_with_thickness[f[j]]

    # 保存 STL 文件
    filename = f"triangle_{index}.stl"
    triangle_mesh.save(filename)
    print(f"已生成 {filename}，面积 {25}~{50}，位于不同象限")

# 生成 100 个不同的三角形 STL
for i in range(100):
    triangle = generate_random_triangle()
    create_stl(triangle, i)

