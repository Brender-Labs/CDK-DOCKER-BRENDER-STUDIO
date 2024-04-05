import bpy
import os

output_path = os.environ.get('EFS_BLENDER_OUTPUT_FOLDER_PATH')

def render_still(active_frame):
    # Seteamos el frame a renderizar    
    bpy.context.scene.frame_set(active_frame)

    # Imprimimos el valor de output_path
    print("Valor de output_path:", output_path)

    # Seteamos el output path para renderizar según el tipo de render
    render_file_path = os.path.join(output_path, f"{active_frame:05d}")
    
    # Imprimimos el valor de render_file_path
    print("Valor de render_file_path:", render_file_path)

    # Seteamos el filepath para el renderizado
    bpy.context.scene.render.filepath = render_file_path

    # Renderizamos la imagen
    bpy.ops.render.render(write_still=True)

# import bpy
# import os

# output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']

# def render_still(active_frame):
#     # Seteamos el frame a renderizar    
#     bpy.context.scene.frame_set(active_frame)

#     # Seteamos el output path para renderizar sugun el tipo de render
#     bpy.context.scene.render.filepath = os.path.join(output_path, f"{active_frame:05d}")

#     # Renderizamos la imagen
#     bpy.ops.render.render(write_still=True)
    