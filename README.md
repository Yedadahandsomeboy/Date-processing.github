具体情况：使用一个基于卷积神经网络的CFD计算模型，该模型可以同时计算流体流过任意障碍物的流场。

优点：该方法在保证精度的情况下，比传统的CFD方法快了3个数量级.同时计算ux、uy、p。

实现方法：输入计算域中障碍物的符号距离函数（SDF）、计算域边界的SDF和流动区域的标签，输出为流体的x方向速度、y方向速度以及流体压强。运用该模型进行训练，得出成熟的模型后便可对任意障碍物的流场计算。

本项目的代码主要用于处理数据集（OpenFoam得到），数据集分为上述的datex：三个sdf；datey：ux、uy、p。

对于DateY.py:该代码的作用是，使用fluidfoam库来读取openfoam算例的非结构网格信息，并读取指定时间步文件的 U、P与网格点对应，进行插值成模型输出数据集的shape（n，3，x，y）。

对于DateX_SDF.py:该代码使用skfmm库加载掩盖码信息，能够准确快速的计算出SDF函数，这里需要提前计算出计算域和障碍物的mask.pkl。

对于blockmeshdict.cc：这是openfoam的文件，指定不变的计算域（-100，-60）（160，60）单位为mm，只需要用代码生成不同的障碍物（基础障碍物为五个形状：圆、前后三角形、菱形、正方形），再运用snappyhexmesh将障碍物映射到背景网格的指定位置，
抠出障碍物的形状（这一步非常容易出错地是，snappyhexmesh是一个三维工具，所以我在用代码生成障碍物.stl文件时，一定要生成厚度跟blockmeshdict的一样，一般openfoam默认二维的模型厚度为1）。

对于make_model_stl.py：该代码的作用是生成三角形障碍物的stl文件，能随机生成100个不同的三角形，后续需要三角形中心在背景网格的原点（0，0），厚度定义为1mm。生成后复制到算例的constant/trisurface文件。

对于4_stl.py：这个代码则是随机生成四边形的stl文件，定义四边形的四个点在四个象限的某一范围内，则可得到n个不同的四边形，后续也可用来生成随机五边形，六边形。

对于make_mask.py:该代码的作用是把障碍物放入背景网格之后，计算他的mask函数，用于计算SDF时使用。

对于read_mask.py:该代码用于检测生成的mask是否符合对应的算例。

环境、依赖包的安装（确保python已经安装）：使用vs code或者pycharm软件，进行新建项目，在项目下面创建环境文件夹venv，接下来在终端处使用命令cd到venv文件下开始安装下载所需的依赖。

①fluodfoam库，在终端使用pip install fluidfoam进行安装，根据https://fluidfoam.readthedocs.io/en/latest/提供的代码中，我们选取符合我们需求能够读取openfoam算例的网格数据，并且进行插值的代码，即DateY.py。
②numpy，该库用于将数据处理成numpy数组，安装方案为在终端输入命令pip install numpy。
③matplotlib，该库在这里用于插值后的数据可视化，使用命令pip install matplotlib安装。
④scipy，使用命令pip install scipy安装。
⑤skfmm，同样的为pip install skfmm 该库用于加载掩盖码信息快速生成SDF函数。
⑥pickle，该库用于读取pkl文件，安装方法为pip install pickle。
⑦trimesh，用于读取stl文件，安装方法为 pip install trimesh。
⑧stl，用于生成stl文件，安装方法为pip install stl。

以上所有的库就是该项目所需要安装的，接下来安装完毕，进行代码编写，在新建项目下面新建py文件，用于编写以上所有代码，在运行代码之前，在终端启动环境，直接输入命令.venv\Scripts\activate即可，然后就可以运行代码了。

运行顺序：第一使用代码make_model_stl.py生成三角形模型stl文件，在4_stl.py则是用来生成四边形模型；第二使用已经修改完成尺寸要求的blockmeshdict文件生成背景网格；第三使用openfoam的sanppyhexmesh在背景网格中扣除make_model_stl.py或4_stl.py生成的模型，得到计算域的网格，并及进行计算；第四使用DateY.py读取并处理openfoam的计算结果；第五使用make_mask.py读取计算域的集合，生成掩盖码信息；第六使用DateX_SDF.py读取生成的掩盖码信息文件并进行SDF函数计算，后处理成所需要的numpy类型（n，3，x，y）。
