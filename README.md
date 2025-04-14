# __关于此项目__

使用一个基于卷积神经网络的CFD计算模型，该模型可以同时计算流体流过任意障碍物的二维流场。优点：该模型在保证精度的情况下，比传统的CFD方法快了3个数量级。且能够同时计算流场的ux、uy、p。  

 实现方法：输入计算域中障碍物的符号距离函数（SDF）、计算域边界的SDF和流动区域的标签；输出为流体的x方向速度、y方向速度以及流体压强。用openfoam计算得出前面所说的输入、输出数据训练集，对该模型进行训练，得出成熟的模型后便可对任意障碍物的流场计算。

该repository的代码主要用于处理数据集（OpenFoam-v2012得到），数据集分别为上述的datex：三个sdf；datey：ux、uy、p。

## **该repository的各个代码的作用** 

**对于make_stl.py：** 文件位于`constant/trisurface`目录中，该代码的作用是随机生成三角形或者四边形障碍物的stl文件，后续需要三角形中心在背景网格的原点（0，0），厚度定义为1mm。文件运行后将在当前目录生成一个`wall.stl`文件。

**openfoam**  包含OpenFOAM的所有配置文件，流体区域均已固定为（-50， -60， 0）至（210， 60， 1），单位米，使用simpleFoam模型计算结果。

**对于PostProcess.py：** 使用fluidfoam库来读取openfoam算例的非结构网格信息，并读取指定时间步文件的 U、P与网格点对应，进行插值成模型输出数据集的shape（1，3，x，y）。使用trimesh计算整个区域的mask数据。使用skfmm计算整个区域的SDF数据。


## **环境、依赖包的安装（确保python已经安装）** 

使用vs code或者pycharm软件，进行新建项目，在项目下面创建环境文件夹venv，接下来在终端处使用命令`cd`到venv文件下开始安装下载所需的依赖。如下

1. fluodfoam库，在终端使用`pip install fluidfoam`进行安装，根据 [https://fluidfoam.readthedocs.io/en/latest] 提供的代码选取符合项目需求的能够读取openfoam算例的网格数据，并且能够进行插值的代码，即DateY.py。

2. numpy，该库用于将所数据处理成numpy数组，安装方案为在终端输入命令`pip install nump`。 

3. matplotlib，该库在这里用于插值后的数据可视化，使用命令`pip install matplotlib`安装。

4. scipy，使用命令`pip install scipy`安装。 

5. skfmm，同样的为`pip install scikit-fmm`该库用于加载掩盖码信息快速生成SDF函数。

6. trimesh，用于读取stl文件，安装方法为 `pip install trimesh`。

7. stl，用于生成stl文件，安装方法为`pip install numpy-stl`。

以上是需要额外安装的python依赖。

可以依次输入`pip install`安装，或者使用`pip install -r requirements.txt`安装所有。

在终端启动环境，直接输入命令`.venv\Scripts\activate`即可，然后就可以运行代码了。

## **运行顺序** 

```shell
# activate environment
source ./venv/bin/activate

# generate stl file
cd ./constant/trisurface
python make_stl.py

# run openfoam
cd ../../
foamCleanTutorial
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite
cp 0.orig/* 0/
simpleFoam

# save data for machine learning
python PostProcess.py
```
