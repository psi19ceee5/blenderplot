#!/bin/bash

FPS=5
SEC=1

FRAMES=$(echo "$FPS * $SEC" | bc)

for (( i=0; i<=$FRAMES; i++ )); do
  blender -b 4Dplot.blend -o //renders/ --python script.py -f $i  -- $i $FRAMES $SEC
done
