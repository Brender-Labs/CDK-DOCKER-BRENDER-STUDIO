import os
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
import boto3.session

bucket_name = os.environ.get('BUCKET_NAME')
bucket_key = os.environ.get('BUCKET_KEY')


def generate_presigned_urls(region):
    try:
        # Crear un cliente de IAM
        iam_client = boto3.client('iam', region_name=region)

        # Nombre del rol que deseas asumir
        role_name = 'RoleForPresharedURL'

        # Verificar si el rol existe
        try:
            iam_client.get_role(RoleName=role_name)
        except iam_client.exceptions.NoSuchEntityException:
            print(f"El rol '{role_name}' no existe. Creando rol...")

            # Crear el rol
            iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument='''{
                  "Version": "2012-10-17",
                  "Statement": [{
                    "Effect": "Allow",
                    "Principal": {
                      "Service": "sts.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                  }]
                }'''
            )
            print(f"Rol '{role_name}' creado correctamente.")

        # Crear un cliente de STS
        sts_client = boto3.client('sts',region_name=region)

        # Obtener el ARN del rol
        role_arn = f'arn:aws:iam::{sts_client.get_caller_identity()["Account"]}:role/{role_name}'

        print(f"ARN del rol: {role_arn}")

        # Asumir el rol para obtener credenciales temporales
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='AssumedRoleSession'
        )

        # Obtener las credenciales temporales
        credentials = assumed_role['Credentials']

        print(f"Credenciales temporales obtenidas correctamente: {credentials}")

        # Crear un nuevo cliente S3 con las credenciales temporales
        s3_client = boto3.client(
            's3',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=region
        )

        # Generar URL prefirmada para thumbnail
        thumbnail_presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{bucket_key}/bs_thumbnail.png"
            },
            ExpiresIn=604800 # 1 semana
        )

        # Generar URL prefirmada para output.zip
        output_zip_presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{bucket_key}/output.zip"
            },
            ExpiresIn=604800 # 1 semana
        )

        return thumbnail_presigned_url, output_zip_presigned_url
    except ClientError as e:
        print(f"Error: {e.response['Error']['Code']}")
        return None, None