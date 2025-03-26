import numpy as np
import stl
from stl import mesh
import random

def generate_random_quadrilateral():
    while True:
        # print("正在生成四边形...")  # 观察是否卡在这里
        # 生成四个顶点，确保分别位于不同象限(单位：毫米)
        x1, y1 = random.uniform(-5, 0), random.uniform(0, 5)   # 第二象限
        x2, y2 = random.uniform(0, 5), random.uniform(0, 5)    # 第一象限
        x3, y3 = random.uniform(0, 5), random.uniform(-5, 0)   # 第四象限
        x4, y4 = random.uniform(-5, 0), random.uniform(-5, 0)  # 第三象限
        
        # 计算四边形面积（通过对角线拆分为两个三角形），单位：平方毫米
        area1 = abs((x1 * (y2 - y4) + x2 * (y4 - y1) + x4 * (y1 - y2)) / 2)
        area2 = abs((x2 * (y3 - y4) + x3 * (y4 - y2) + x4 * (y2 - y3)) / 2)
        total_area = area1 + area2
        # print(f"生成的面积: {total_area}")  # 打印面积，看看是否符合条件

        if 50 <= total_area <= 100:
            return np.array([[x1, y1, 0], [x2, y2, 0], [x3, y3, 0], [x4, y4, 0]])

def create_stl(quadrilateral_vertices, index, thickness=1): # 厚度单位：毫米
    # 复制并增加厚度
    vertices_with_thickness = np.vstack([
        quadrilateral_vertices,
        quadrilateral_vertices + [0, 0, thickness]  # 平移 Z 方向增加厚度
    ])
    print(f"模型 {index} 顶点坐标:\n", vertices_with_thickness)  # **检查顶点是否有厚度**

    # 定义面（拆分成两个三角形）
    faces = [
        [0, 1, 2], [0, 2, 3],  # 底部
        [4, 5, 6], [4, 6, 7],  # 顶部
        [0, 1, 5], [0, 5, 4],  # 侧面1
        [1, 2, 6], [1, 6, 5],  # 侧面2
        [2, 3, 7], [2, 7, 6],  # 侧面3
        [3, 0, 4], [3, 4, 7]   # 侧面4
    ]

    # 创建 STL mesh
    quad_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            quad_mesh.vectors[i][j] = vertices_with_thickness[f[j]]

    # 保存 STL 文件
    filename = f"quadrilateral_{index}.stl"
    quad_mesh.save(filename)
    print(f"已生成 {filename}，面积 {50}~{100}，四个顶点分别位于不同象限")

# print("开始批量生成 200 个 STL...")
# 生成 200 个不同的四边形 STL
for i in range(1):
    quadrilateral = generate_random_quadrilateral()
    create_stl(quadrilateral, i)
