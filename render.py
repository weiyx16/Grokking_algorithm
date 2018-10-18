# This script is an example of how you can run blender from the command line
# (in background mode with no interface) to automate tasks, in this example it
# creates a text object, camera and light, then renders and/or saves it.
# This example also shows how you can parse command line options to scripts.
#
# Example usage for this test.
#  blender --background --factory-startup --python $HOME/background_job.py -- \
#          --text="Hello World" \
#          --render="/tmp/hello" \
#          --save="/tmp/hello.blend"\
#          --bground="/file"
#
# Notice:
# '--factory-startup' is used to avoid the user default settings from
#                     interfering with automated scene generation.
#
# '--' causes blender to ignore all following arguments so python can use them.
#
# See blender --help for details.

## --- use::
# blender --background --factory-startup --python ~/3D_render/render.py --save = "~/Desktop" --bground = "~/Desktop/1.png" --smpl = "/Desktop/hello_smpl/obj"

import bpy
# import random as rd 
# import math
import os

def render_function(save_path, background_path, smpl_path):

    # Clear existing objects.
    bpy.ops.wm.read_factory_settings(use_empty=True)

    scene = bpy.context.scene

    # Camera
    cam_data = bpy.data.cameras.new("MyCam")
    cam_ob = bpy.data.objects.new(name="MyCam", object_data=cam_data)
    scene.objects.link(cam_ob)  # instance the camera object in the scene
    scene.camera = cam_ob       # set the active camera
    cam_ob.location = 2.0, -2.0, 1.0

    # Lamp
    lamp_data = bpy.data.lamps.new("MyLamp", 'POINT')
    lamp_ob = bpy.data.objects.new(name="MyCam", object_data=lamp_data)
    scene.objects.link(lamp_ob)
    lamp_ob.location = 3.0, -0.5, 1.0

    # if background_path:
    '''
    img = bpy.data.images.load(filepath=background_path,check_existing=False)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space_data = area.spaces.active
            bg = space_data.background_images.new()
            bg.image = img
            break
    # or maybe in this:
    '''
    bg_dir, bg_name = os.path.split(background_path)
    bpy.context.space_data.show_background_images = True
    bpy.ops.image.open(filepath=background_path, directory = bg_dir, files=[{"name":bg_name,"name":bg.name}],relative_path = True, show_multiview = False)
    # read image size
    # bpy.data.scenes["scene"].render.resolution_x = 
    # bpy.data.scenes["scene"].render.resolution_y =

    # if smpl_path:
    bpy.ops.import_scene.obj(filepath=smpl_path)
    
    _ , smpl_name = os.path.split(smpl_path)
    ## use when the blender need't the extension
    smpl_name = smpl_name[0:-4]

    '''
    bpy.data.objects[smpl_name].location = 0,0,0
    # random rotation the smpl
    random_angle = [rd.randint(-math.pi/2,math.pi/2) for i in range(3)]
    bpy.data.objects[smpl_name].rotation_euler(angles=random_angle ,order='XYZ')
    '''
    
    bpy.context.space_data.context = 'WORLD'
    bpy.context.scene.world.use_sky_paper = True

    bpy.context.space_data.context = 'TEXTURE'
    bpy.ops.texture.new()
    bpy.ops.image.open(filepath=background_path, directory = bg_dir, files=[{"name":bg_name,"name":bg_name}], show_multiview = False)
    bpy.context.scene.world.texture_slots[0].use_map_horizon = True
    
    # render the image
    bpy.context.space_data.context = 'RENDER'
    bpy.ops.render.render()


    # if save_path:
    # save the rendered image
    save_file_name = smpl_name + '.png'
    save_path = save_path + save_file_name
    bpy.ops.image.save_as(save_as_render = True, copy = True, filepath=save_path, relative_path = True, show_multiview = False, use_multiview = False)

'''
    if render_path:
        render = scene.render
        render.use_file_extension = True
        render.filepath = render_path
        bpy.ops.render.render(write_still=True)
'''

def main():
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message

    # get the args passed to blender after "--", all of which are ignored by
    # blender so scripts may receive their own arguments
    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    # When --help or no args are given, print this help
    usage_text = (
            "Run blender in background mode with this script:"
            "  blender --background --python " + __file__ + " -- [options]"
            )

    parser = argparse.ArgumentParser(description=usage_text)

    # input the arguments needed

    parser.add_argument("-s", "--save", dest="save_path", metavar='FILE',
            help="Save the generated file to the specified path")
    #parser.add_argument("-r", "--render", dest="render_path", metavar='FILE',
            #help="Render an image to the specified path")
    parser.add_argument("-bg", "--bground", dest="background_path", metavar='FILE',
            help="Read the background file from the specified path")
    parser.add_argument("-smpl", "--smpl", dest="smpl_path", metavar='FILE',
            help="Read the smpl file from the specified path")

    args = parser.parse_args(argv)  # In this example we wont use the args

    if not argv:
        parser.print_help()
        return

    if not args.save_path  or not args.background_path or not args.smpl_path:
        print("Error: some arguments are not given, aborting.")
        parser.print_help()
        return

    # Run the example function
    render_function(args.save_path, args.background_path, args.smpl_path)

    print("batch job finished, exiting")


if __name__ == "__main__":
    main()
