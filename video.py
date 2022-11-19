import bpy
import sys
import os
import math
import numpy as np

def conv_dir_bpy(dir) :
    if dir.startswith('.') :
        dir = dir[1:]
        dir = '/' + dir

    if not dir.endswith('/') :
        dir = dir + '/'

    return dir

def main() :

    argdir = sys.argv[11]
    argsec = float(sys.argv[12])

    for window in bpy.context.window_manager.windows :
        screen = window.screen

    for area in screen.areas :
        if area.type == 'SEQUENCE_EDITOR' :
            override = bpy.context.copy()
            override['area'] = area
            break

    with bpy.context.temp_override(**override) :

        # TODO
        #  - generate list of files with e.g. .png extension
        #  - assign tot_frames from length of list of files
        #  ? how to generate a context (currently 'None'?) to
        #    assign it to SEQUENCE_EDITOR?

        images = []
        filelist = os.listdir(argdir)
        filelist.sort()
        for file in filelist :
            if file.endswith(".png") :
                images.append(file)

        img_dic = [{'name': item} for item in images]
        
        tot_frames = len(images)
        seconds = argsec

        fps = tot_frames/seconds

        directory = conv_dir_bpy(argdir)
        bpy.ops.sequencer.image_strip_add(directory=directory, files=img_dic)

        scene = bpy.context.scene
        scene.render.fps = math.floor(fps)
        scene.frame_start = 0
        scene.frame_end = tot_frames - 1
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
        scene.render.filepath = '//video/'

        #bpy.ops.wm.save_as_mainfile(filepath='//4DplotVE.blend')

if __name__ == "__main__" :
    main()
