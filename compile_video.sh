#!/bin/bash

DIR='./renders'
SEC=4

blender -b 4DplotVE.blend -o //video/ --python video.py -f 1 -a -- $DIR $SEC
