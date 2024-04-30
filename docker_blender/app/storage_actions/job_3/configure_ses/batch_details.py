import boto3
from datetime import datetime, timedelta

def get_batch_job_2_details(job_id, region):
    try:
        # Crear cliente de AWS Batch
        batch_client = boto3.client('batch', region_name=region)

        # Obtener detalles del trabajo
        response = batch_client.describe_jobs(jobs=[job_id])

        # Verificar si se recibió una respuesta válida
        if 'jobs' not in response or len(response['jobs']) == 0:
            raise ValueError(f"No se encontraron detalles para el trabajo con ID {job_id}")

        # Extraer información sobre el trabajo de AWS Batch
        job_info = response['jobs'][0]

        print(f"Job info: {job_info}")

        # Verificar si se proporcionaron las claves necesarias
        if 'startedAt' not in job_info or 'stoppedAt' not in job_info:
            raise ValueError("La respuesta de AWS Batch no contiene la información necesaria")

        # Extraer tiempo de inicio y finalización del trabajo
        start_time_ms = job_info['startedAt']
        end_time_ms = job_info['stoppedAt']

        # Convertir de milisegundos a segundos
        start_time_seconds = start_time_ms / 1000
        end_time_seconds = end_time_ms / 1000

        # Convertir a objetos datetime
        start_datetime = datetime.utcfromtimestamp(start_time_seconds)
        end_datetime = datetime.utcfromtimestamp(end_time_seconds)

        # Calcular tiempo de ejecución
        runtime_seconds = (end_datetime - start_datetime).total_seconds()
        runtime_timedelta = timedelta(seconds=runtime_seconds)

        # Obtener horas, minutos y segundos
        hours = runtime_timedelta.seconds // 3600
        minutes = (runtime_timedelta.seconds % 3600) // 60
        seconds = runtime_timedelta.seconds % 60

        runtime_formatted = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

        return runtime_formatted
    
    except Exception as e:
        print(f"Ocurrió un error al obtener detalles del trabajo: {e}")
        return None
