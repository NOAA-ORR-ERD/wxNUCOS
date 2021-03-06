#!/bin/bash

# script to build assorted icon files

## build the python files with img2py

img2py -n NOAA64 NOAA-Meatball-text64.png ../Icons.py
img2py -a -n NUCOS64 NUCOS-64.png ../Icons.py
img2py -a -n NUCOS16 NUCOS-16.png ../Icons.py


## build the Windows Icon with png2icon
echo "Building Windows icon file"
png2ico NUCOS.ico NUCOS-16.png NUCOS-32.png NUCOS-48.png NUCOS-128.png 



