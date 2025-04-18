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
snappyHexMesh -overwrite
cp 0.orig/* 0/
simpleFoam

# save data for machine learning
python PostProcess.py