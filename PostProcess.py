import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from fluidfoam import readvector, readscalar, readmesh
import h5py
import trimesh  # 用于读取 STL 文件
import skfmm

sol = 'openfoam'

x, y, z = readmesh(sol)

timename = '100'  #时间步
vel = readvector(sol, timename, 'U')
pressure = readscalar(sol, timename, 'p')

print("前5个网格点:", x[:5], y[:5])
print("pressure 读取成功, 其前5个值:", pressure[:5] if pressure is not None else "读取失败")
print("pressure 数组长度:", len(pressure) if pressure is not None else "读取失败")

# 设置网格大小
ngridx = 520
ngridy = 240

xinterpmin = x.min() + 1e-6  # 避免刚好落在边界外
xinterpmax = x.max() - 1e-6
yinterpmin = y.min() + 1e-6
yinterpmax = y.max() - 1e-6

xi = np.linspace(xinterpmin, xinterpmax, ngridx)
yi = np.linspace(yinterpmin, yinterpmax, ngridy)

xinterp, yinterp = np.meshgrid(xi, yi)

points = np.vstack((x, y)).T  
print("网格点数:", len(x))
print("y点数:", len(y))

pressure_i = griddata(points, pressure, (xinterp, yinterp), method="nearest")
velx_i = griddata(points, vel[0, :], (xinterp, yinterp), method="nearest")
vely_i = griddata(points, vel[1, :], (xinterp, yinterp), method="nearest")
print("pressure_i 插值成功, 其前5个值:", pressure_i.flatten()[:5])
print("velx_i 插值成功, 其前5个值:", velx_i.flatten()[:5])
print("vely_i 插值成功, 其前5个值:", vely_i.flatten()[:5])

result = np.stack([velx_i.T, vely_i.T, pressure_i.T ], axis=0)
result = result[np.newaxis, ...]   # shape (1, 3, 520, 240)

# save result as hdf5
with h5py.File("p_v.h5", "w") as f:
    f.create_dataset("data", data=result)

################################ Domain mask #########################################
z = (z.min() + z.max())/2.0

# 加载 STL 文件
mesh = trimesh.load_mesh('openfoam/constant/triSurface/wall.stl')

# 初始化掩码数组
mask = np.zeros((ngridx, ngridy), dtype=int)

for i in range(len(xi)):
    for j in range(len(yi)):
            point = np.array([xi[i], yi[j], z])
            # 判断点是否在几何体内
            if mesh.contains([point]):
                mask[i, j] = 1  # 标记为几何体区域

#### for debug, show mask result
# import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
# cmap = ListedColormap(['red', 'blue'])
# plt.imshow(mask, cmap=cmap)  # 灰度显示
# plt.colorbar()
# plt.title("Mask Visualization")
# plt.show()

############################# SDF ###############################
# 计算 障碍物SDF、边界条件、计算域SDF
sdf = mask.copy()
sdf[sdf == 1] = -1
sdf[sdf == 0] = 1
sdf_obstacle = skfmm.distance(sdf, dx=1.0) #障碍物sdf

boundary_mask = mask.copy() 
#设置边界条件
boundary_condition = {"obstacle":0, "flow":1, "non-slip":2, "inlet":3, "outlet":4}
boundary_mask[sdf == -1] = boundary_condition["obstacle"]
boundary_mask[sdf == 1] = boundary_condition["flow"]
boundary_mask[0, :] = boundary_condition["non-slip"]   # 上边界
boundary_mask[-1, :] = boundary_condition["non-slip"]  # 下边界
boundary_mask[:, 0] = boundary_condition["inlet"]      # 左边界
boundary_mask[:, -1] = boundary_condition["outlet"]    # 右边界
#sdf = skfmm.distance(sdf)

sdf[sdf == -1] = 1
sdf[:, 0] = -1  
sdf[:, -1] = -1 

sdf_domain = skfmm.distance(sdf, dx=1.0)  # 计算域SDF
###########################################################
# # # 保存数据到 hdf5 文件
mask_sdf = np.stack([sdf_obstacle, boundary_mask,sdf_domain ], axis=0)
mask_sdf = mask_sdf[np.newaxis, ...]   # shape (1, 3, 520, 240)

with h5py.File("mask_sdf.h5", "w") as f:
    f.create_dataset("mask_sdf", data=mask_sdf)
