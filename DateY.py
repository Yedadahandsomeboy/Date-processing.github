from fluidfoam import readmesh
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from fluidfoam import readvector, readscalar

sol = '../yuan'

x, y, z = readmesh(sol)

timename = '0.005'  #时间步
vel = readvector(sol, timename, 'U')
alpha = readscalar(sol, timename, 'p')

print("前5个网格点:", x[:5], y[:5])
print("alpha 读取成功, 其前5个值:", alpha[:5] if alpha is not None else "读取失败")
print("alpha 数组长度:", len(alpha) if alpha is not None else "读取失败")

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

alpha_i = griddata(points, alpha, (xinterp, yinterp), method="nearest")
velx_i = griddata(points, vel[0, :], (xinterp, yinterp), method="nearest")
vely_i = griddata(points, vel[1, :], (xinterp, yinterp), method="nearest")
print("alpha_i 插值成功, 其前5个值:", alpha_i.flatten()[:5])
print("velx_i 插值成功, 其前5个值:", velx_i.flatten()[:5])
print("vely_i 插值成功, 其前5个值:", vely_i.flatten()[:5])

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)  # 10x6 英寸，150 DPI  #创建窗口、分辨率
plt.rcParams.update({'font.size': 10})       #字体标签刻度
plt.xlabel('x')
plt.ylabel('y')
d = 1    #归一化尺度
plt.title("Contour Plot of α", fontsize=16, fontweight='bold')  # 标题

CS = plt.contourf(xi/d, yi/d, alpha_i)

cbar = fig.colorbar(CS)
cbar.ax.set_ylabel

plt.show()

print("x 范围:", x.min(), x.max())
print("y 范围:", y.min(), y.max())
print("插值网格范围:", xinterpmin, xinterpmax, yinterpmin, yinterpmax)
print("x 第一个值:", x[0], "单位: 米 还是 毫米？")
print("x 形状:", x.shape)
print("y 形状:", y.shape)
print("alpha 形状:", alpha.shape)

result = np.array([alpha_i, velx_i, vely_i]).reshape(1, 3, ngridx, ngridy)
