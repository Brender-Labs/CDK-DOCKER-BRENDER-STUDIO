import bpy
import os

output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']

def render_still(active_frame):
    # Seteamos el frame a renderizar    
    bpy.context.scene.frame_set(active_frame)

    # Seteamos el output path para renderizar sugun el tipo de render
    bpy.context.scene.render.filepath = os.path.join(output_path, f"{active_frame:05d}")

    # Renderizamos la imagen
    bpy.ops.render.render(write_still=True)
    