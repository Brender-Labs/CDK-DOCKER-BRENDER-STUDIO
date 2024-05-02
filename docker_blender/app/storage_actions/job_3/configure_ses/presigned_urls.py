import os
import boto3
from botocore.exceptions import ClientError

bucket_name = os.environ.get('BUCKET_NAME')
bucket_key = os.environ.get('BUCKET_KEY')

# review args if needed!!!

def generate_presigned_urls(thumbnail_path, output_zip_path):
    try:
        s3_client = boto3.client('s3')

        # Generate presigned url for thumbnail
        thumbnail_presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{bucket_key}/bs_thumbnail.png"
            },
            ExpiresIn=604800  # 1 week
        )
        # Generate presigned url for output.zip
        output_zip_presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': f"{bucket_key}/output.zip"
            },
            ExpiresIn=604800  # 1 week
        )
        return thumbnail_presigned_url, output_zip_presigned_url
    except ClientError as e:
        print(f"Error: {e.response['Error']['Code']}")
        return None, None 