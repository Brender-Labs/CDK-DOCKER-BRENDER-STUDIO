import boto3
import json
from datetime import datetime, timedelta

def convert_bytes_to_mb(bytes_size):
    """
    Convierte el tamaño de bytes a megabytes (MB)
    """
    mb_size = bytes_size / (1024 * 1024)
    return mb_size

def convert_bytes_to_gb(bytes_size):
    """
    Convierte el tamaño de bytes a gigabytes (GB)
    """
    gb_size = bytes_size / (1024 * 1024 * 1024)
    return gb_size

def send_render_ok_email(thumbnail_presigned_url, output_zip_presigned_url, ses_config, render_details, zip_size, runtime_minutes):
    """
    Send an email with the specified SES configuration and render details
    """
    try:
        ses = boto3.client('ses', region_name=ses_config['region'])
        source_email = ses_config['source_email']
        destination_email = ses_config['destination_email']
        render_ok_template_name = ses_config['render_ok_template_name']

        # Render details
        project_name = render_details['project_name']
        resolution = render_details['resolution']
        scene_name = render_details['scene_name']
        layer_name = render_details['layer_name']
        camera_name = render_details['camera_name']
        samples = render_details['samples']
        engine = render_details['engine']
        render_type = render_details['render_type']

        if zip_size > 1024 * 1024 * 1024:  # Si el tamaño es mayor a 1 GB
            object_size_str = f"{convert_bytes_to_gb(zip_size):.2f} GB"
        else:
            object_size_str = f"{convert_bytes_to_mb(zip_size):.2f} MB"

        # Definir los parámetros de la plantilla
        template_data = {
            'project_name': project_name,
            'resolution': resolution,
            'scene_name': scene_name,
            'layer_name': layer_name,
            'camera_name': camera_name,
            'samples': samples,
            'engine': engine,
            'render_type': render_type,
            'thumbnail_url': thumbnail_presigned_url,
            'alternate_download_url': output_zip_presigned_url,
            'brender_download_url': "brenderstudio.com/download-render?id=" + str(output_zip_presigned_url) + "&project=" + str(project_name) + "&scene=" + str(scene_name) + "&layer=" + str(layer_name) + "&camera=" + str(camera_name) + "&samples=" + str(samples) + "&engine=" + str(engine) + "&render_type=" + str(render_type) + "&resolution=" + str(resolution),
            'rendering_time': runtime_minutes,
            'object_size': object_size_str,
            'current_year': str(datetime.now().year),
            'expiration_time': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')  # 7 days from now 
        }

        # Enviar el correo electrónico utilizando la plantilla
        response = ses.send_templated_email(
            Source=source_email,
            Destination={'ToAddresses': [destination_email]},
            Template=render_ok_template_name,
            TemplateData=json.dumps(template_data)
        )

        print("Correo electrónico enviado con éxito!")
        print("ID de mensaje:", response['MessageId'])

        return response

    except Exception as e:
        # Capturar cualquier excepción y mostrar un mensaje de error
        print("Error al enviar el correo electrónico:", e)
        return None
