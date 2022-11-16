#!/bin/bash

FRAMES=5
SEC=1

blender -b -o //video/ --python video.py -f 1 -a -- $FRAMES $SEC
