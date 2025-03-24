# 原文的代码
import pickle
import skfmm

# 加载掩码数据
mask_data = pickle.load(open('./mask.pkl', "rb"))#加载自己的的mash.pkl文件，在生成blockmeshdict的时候随手生成

# 计算障碍物的 SDF
distance_obstacle = skfmm.distance(mask_data, dx=1.0)

# 定义边界条件
boundary_condition = {"obstacle": 0, "flow": 1, "non-slip": 2, "inlet": 3, "outlet": 4}

# 应用边界条件
mask_data[mask_data == -1] = boundary_condition["obstacle"]
mask_data[mask_data == 1] = boundary_condition["flow"]
mask_data[0] = boundary_condition["non-slip"]
mask_data[-1] = boundary_condition["non-slip"]
mask_data[:, 0] = boundary_condition["inlet"]
mask_data[:, -1] = boundary_condition["outlet"]

# 重新计算 SDF
distance_boundary = skfmm.distance(mask_data, dx=1.0)

# 确保边界条件正确
mask_data[mask_data == -1] = 1
mask_data[0] = -1
mask_data[-1] = -1

# 计算计算域的 SDF
distance_domain = skfmm.distance(mask_data, dx=1.0)
