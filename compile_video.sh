#!/bin/bash

DIR='./renders'
SEC=1

blender -b 4DplotVE.blend -o //video/ --python video.py -f 1 -a -- $DIR $SEC
