#!/bin/bash

FRAMES=24

for (( i=0; i<=$FRAMES; i++ )); do
  blender -b 3dplot.blend --python script.py -f $i -o renders -- $i $FRAMES
done
