import bpy
import sys
import os
from argparse import Namespace
from storage_actions.job_3.animation_ops.animation_parser import create_parser


def main():
    print("bpy script playblast")
    parser = create_parser()

    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    bpy.app.driver_namespace['argv'] = argv
    

    args: Namespace = parser.parse_args(bpy.app.driver_namespace['argv'])

    video_codec = 'H264'  # 'NONE', 'DNXHD', 'DV', 'FFV1', 'FLASH', 'H264', 'HUFFYUV', 'MPEG1', 'MPEG2', 'MPEG4', 'PNG', 'QTRLE', 'THEORA', 'WEBM', 'AV1')
    output_quality = 'MEDIUM'  # 'HIGH', 'MEDIUM', 'LOW'
    encoding_speed = 'GOOD'  # 'GOOD', 'REALTIME', 'BEST'
    autosplit = False 

    print("args:", args)
    res_x = args.resolution_x
    res_y = args.resolution_y

    # Funcion para reescalar la resolucion a un maximo de 720p y que mantenga la relacion de aspecto
    def rescale_resolution(res_x, res_y):
        if res_x > 1280:
            res_y = int((1280 / res_x) * res_y)
            res_x = 1280
        if res_y > 720:
            res_x = int((720 / res_y) * res_x)
            res_y = 720
        return res_x, res_y
    
    res_x, res_y = rescale_resolution(res_x, res_y)

    scene = bpy.context.scene
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y

    scene.render.fps = args.fps
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4' # 'MPEG4'
    scene.render.ffmpeg.codec = video_codec
    scene.render.ffmpeg.constant_rate_factor = output_quality
    scene.render.ffmpeg.ffmpeg_preset = encoding_speed
    scene.render.ffmpeg.use_autosplit = autosplit

    output_folder = os.path.join(args.efs_project_path, 'output')
    print("Output folder:", output_folder)
    playblast_path = args.efs_project_path
    print("Playblast path:", playblast_path)

    # Load images in the sequence editor
    seq = bpy.context.scene.sequence_editor_create()
    images = sorted([f for f in os.listdir(output_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.exr', '.tif', '.tiff', '.bmp', '.tga', '.cin', '.dpx', '.hdr', '.webp'))])

    for index, image in enumerate(images):
        filepath = os.path.join(output_folder, image)
        seq_strip = seq.sequences.new_image(name=image, filepath=filepath, channel=1, frame_start=index+1)

    scene.frame_start = 1
    scene.frame_end = len(images)
    
    # Output file name
    output_filepath = os.path.join(playblast_path, 'bs_playblast_')
    bpy.context.scene.render.filepath = output_filepath

    # Render the animation
    bpy.ops.render.render(animation=True, write_still=True)

if __name__ == "__main__":
    main()