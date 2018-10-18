## --- use::
## add a text in blender and copy it into with a run command
## This code is for render a SMPL on a random image.

import bpy
import random as rd 
import math
import os
import mathutils

def render_function(save_path, background_path, smpl_path):

    # Clear existing objects.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # bpy.context.window.screen = bpy.data.screens['Default']
    scene = bpy.context.scene

    # if background_path:
    # bg_dir, bg_name = os.path.split(background_path)

    img = bpy.data.images.load(filepath=background_path,check_existing=False)
    rv3d = None
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                space_data = area.spaces.active
                rv3d = space_data.region_3d
                space_data.show_background_images = True
                bg = space_data.background_images.new()
                bg.image = img
                break

    # read image size
    # bpy.data.scenes["scene"].render.resolution_x = 
    # bpy.data.scenes["scene"].render.resolution_y =

    # Camera
    cam_data = bpy.data.cameras.new("MyCam")
    cam_ob = bpy.data.objects.new(name="MyCam", object_data=cam_data)
    scene.objects.link(cam_ob)  # instance the camera object in the scene
    scene.camera = cam_ob       # set the active camera
    cam_ob.location = 4.5, -3, 1.0
    cam_ob.select = True 
    cam_ob.rotation_euler = (1.4,0,1)
    rv3d.view_perspective = 'CAMERA' # Go to camera perspective to see your BG iamge



    # Lamp
    lamp_data = bpy.data.lamps.new("MyLamp", 'POINT')
    lamp_ob = bpy.data.objects.new(name="MyCam", object_data=lamp_data)
    scene.objects.link(lamp_ob)
    lamp_ob.location = 3.0, -0.5, 1.0



    # if smpl_path:
    bpy.ops.import_scene.obj(filepath=smpl_path)
    _ , smpl_name = os.path.split(smpl_path)
    ## use when the blender need't the extension
    smpl_name = smpl_name[0:-4]

    # random rotation the smpl
    random_angle = [(rd.random()-0.5)*math.pi for i in range(3)]
    bpy.data.objects[smpl_name].rotation_euler = random_angle
    
    # bpy.context.space_data.context = 'TEXTURE'
    bpy.data.textures.new("Texture",'IMAGE')
    img_texture = bpy.data.images.load(filepath=background_path,check_existing=False)
    bpy.data.textures["Texture"].image = img_texture

    # bpy.context.space_data.context = 'WORLD'
    if scene.world is None:
        # create a new world
        new_world = bpy.data.worlds.new("New World")
        new_world.use_sky_paper = True
        scene.world = new_world
        slot = scene.world.texture_slots.add()
        slot.use_map_horizon = True
        ## important to use this
        slot.texture = bpy.data.textures["Texture"]
        # scene.world.texture_slots[0].use_map_horizon = True
       
    # render the image
    save_file_name = smpl_name + '.png'
    save_path = save_path + save_file_name

    bpy.data.scenes['Scene'].render.filepath = save_path
    bpy.ops.render.render( write_still=True ) 
    # if save_path:
    # save the rendered image
    print('Render over')

def main():
    
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message
    '''
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
    # render_function(args.save_path, args.render_path, args.background_path, args.smpl_path)
    '''

    save_path = '/home/weiyx/Desktop/'
    background_path = '/home/weiyx/Desktop/1.png'
    smpl_path = '/home/weiyx/Desktop/hello_smpl.obj'

    
    render_function(save_path, background_path, smpl_path)
    print("batch job finished, exiting")


if __name__ == "__main__":
    main()
