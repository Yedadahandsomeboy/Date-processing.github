#!/bin/bash

# activate environment
source ./venv/bin/activate

# generate stl file
cd ./constant/trisurface
python make_stl.py

# run openfoam
cd ../../
foamCleanTutorials
blockMesh
surfaceFeatureExtract
decomposePar -fileHandler collated
mpirun -np 12 snappyHexMesh -parallel -overwrite -fileHandler collated
reconstructParMesh -constant
cp 0.orig/* 0/
decomposePar -latestTime -force
mpirun -np 12 simpleFoam -parallel -fileHandler collated
reconstructPar
rm -rf processor*

# save data for machine learning
python PostProcess.py

