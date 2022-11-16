#!/bin/bash

blender -b 4Dplot.blend -o //renders/ --python script.py -f 1 -- 1 1 1
