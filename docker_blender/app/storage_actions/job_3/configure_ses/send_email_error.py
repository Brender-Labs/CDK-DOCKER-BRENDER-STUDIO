import boto3
import json
from datetime import datetime, timedelta
from urllib.parse import quote_plus

def send_render_error_email(ses_config, render_details, runtime_minutes, status):
    """
    Send an email with the specified SES configuration and render details if render fails
    """
    try:
        ses = boto3.client('ses', region_name=ses_config['region'])
        source_email = ses_config['source_email']
        destination_email = ses_config['destination_email']
        render_error_template_name = ses_config['render_error_template_name']

        # Render details
        project_name = render_details['project_name']
        resolution = render_details['resolution']
        scene_name = render_details['scene_name']
        layer_name = render_details['layer_name']
        camera_name = render_details['camera_name']
        samples = render_details['samples']
        engine = render_details['engine']
        render_type = render_details['render_type']

        # Obtener la razón del estado
        status_reason = status['reason']
        log_stream_name = status['log_stream_name']

        # Transformar las barras diagonales en el formato adecuado para la URL
        log_stream_name_encoded = quote_plus(log_stream_name)

        # Construir la URL con el log_stream_name codificado
        log_link = f"https://{ses_config['region']}.console.aws.amazon.com/cloudwatch/home?region={ses_config['region']}#logsV2:log-groups/log-group/%2Faws%2Fbatch%2Fjob/log-events/{log_stream_name_encoded}"

        # https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%2Faws%2Fbatch%2Fjob/log-events/JobDefinition_VERSION__4_1_1__4c448378-ef8e-435b-b65f-50c20f9a2f9f%2Fdefault%2F7c6ec4481fcb4cb1890f92e8b6e37ecb

        # Definir los parámetros de la plantilla
        template_data = {
            'project_name': project_name,
            'reason_message': status_reason,
            'log_link': log_link,
            'resolution': resolution,
            'scene_name': scene_name,
            'layer_name': layer_name,
            'camera_name': camera_name,
            'samples': samples,
            'engine': engine,
            'render_type': render_type,
            'execution_time': runtime_minutes,
            'current_year': str(datetime.now().year),
        }

        print("template_data:", template_data)

        # Enviar el correo electrónico utilizando la plantilla
        response = ses.send_templated_email(
            Source=source_email,
            Destination={'ToAddresses': [destination_email]},
            Template=render_error_template_name,
            TemplateData=json.dumps(template_data)
        )

        print("Correo electrónico enviado con éxito!")
        print("ID de mensaje:", response['MessageId'])

        return response

    except Exception as e:
        # Capturar cualquier excepción y mostrar un mensaje de error
        print("Error al enviar el correo electrónico:", e)
        return None