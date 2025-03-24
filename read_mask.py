import pickle
import numpy as np
import matplotlib.pyplot as plt

# 读取 pkl 文件
with open("mask2.pkl", "rb") as f:
    mask = pickle.load(f)

# 检查数据类型
if isinstance(mask, np.ndarray):
    print("Mask 形状:", mask.shape)
    plt.imshow(mask, cmap="gray")  # 灰度显示
    plt.colorbar()
    plt.title("Mask Visualization")
    plt.show()
else:
    print("mask.pkl 不是 NumPy 数组，而是", type(mask))
