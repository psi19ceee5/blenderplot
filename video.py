import bpy
import sys
import math
import numpy as np

def main() :
    
    # TODO
    #  - generate list of files with e.g. .png extension
    #  - assign tot_frames from length of list of files
    #  ? how to generate a context (currently 'None'?) to assign it to SEQUENCE_EDITOR?
    
    tot_frames = int(sys.argv[10])
    seconds = float(sys.argv[11])
    
    fps = tot_frames/seconds
    
    # Delete Cube
    bpy.ops.object.delete(use_global=False, confirm=False)

    bpy.context.area.ui_type = 'SEQUENCE_EDITOR'
    
    bpy.ops.sequencer.image_strip_add(directory="//renders/")
    
    scene = bpy.context.scene
    scene.render.fps = math.floor(fps)
    scene.frame_start = 1
    scene.frame_end = tot_frames
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmped.format = 'MPEG'
    scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
    scene.render.filepath = '//video/'

    bpy.ops.wm.save_as_mainfile(filepath='//4DplotVE.blend')

if __name__ == "__main__" :
    main()