import os
from PIL import Image

def generate_thumbnail(render_output_path, thumbnail_output_path):
    # Crear thumbnail de la primera imagen que haya en output, guardarlo en la misma ruta de files (efs project path env) como: _thumbnail.png
    print("Creating thumbnail...")
    # Encontrar la primera imagen en la carpeta de output
    image_path = None
    for root, dirs, files in os.walk(render_output_path):
        for file in files:
            if file.endswith(('.bmp', '.iris', '.png', '.jpg', '.jpeg', '.jp2', '.tga', '.dpx', '.exr', '.hdr', '.tif', 'tiff','.webp')):
                image_path = os.path.join(root, file)
                break
        if image_path:
            break
    if not image_path:
        raise FileNotFoundError(f"No image found in {render_output_path}")

    # Abrir la imagen y crear el thumbnail
    image = Image.open(image_path)

    # Calcular las nuevas dimensiones manteniendo el aspect ratio
    width, height = image.size
    new_width = 500
    new_height = int((height / width) * new_width)

    # Redimensionar la imagen con las nuevas dimensiones
    thumbnail = image.resize((new_width, new_height))
    # thumbnail_path = os.path.join(os.path.dirname(image_path), 'thumbnail.png')
    thumbnail_path = os.path.join(thumbnail_output_path, '_thumbnail.png')
    thumbnail.save(thumbnail_path)
    print(f"Thumbnail created: {thumbnail_path}")
    return thumbnail_path
