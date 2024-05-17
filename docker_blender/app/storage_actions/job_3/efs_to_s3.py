import os
import sys
from app_utils.parse_json import parse_json
from output_ops.generate_thumbnail import generate_thumbnail
from output_ops.output_to_zip import output_to_zip
from output_ops.upload_s3 import upload_to_s3
from configure_ses.presigned_urls import generate_presigned_urls
from configure_ses.send_email import send_render_ok_email
from configure_ses.send_email_error import send_render_error_email
from clean_up.clean_project_efs import clean_up_project_folder_efs
from configure_ses.batch_details import get_batch_job_info

def main():
    try:
        # Ensure required environment variables are present
        required_env_vars = ['BUCKET_NAME', 'BUCKET_KEY', 'EFS_BLENDER_FOLDER_PATH']
        for env_var in required_env_vars:
            if env_var not in os.environ:
                raise ValueError(f"Missing environment variable: {env_var}")

        bucket_key = os.environ['BUCKET_KEY']
        efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']
        render_output_path = os.path.join(efs_path, bucket_key, 'output') # example: /mnt/efs/projects/project_5/output
        thumbnail_output_path = os.path.join(efs_path, bucket_key) # example: /mnt/efs/projects/project_5

        # Parse JSON 
        ses_json_str = sys.argv[1]

        if len(sys.argv) > 2:
            print("Error, no json string provided")
            sys.exit(1)

        json_ses = parse_json(ses_json_str)
        print("Parsed JSON SES:", json_ses)

        ses_details = json_ses['ses']
        ses_active = json_ses['ses']['ses_active']
        ses_config = json_ses['ses']['ses_config']
        render_details = json_ses['ses']['render_details']
        region = ses_config['region']
        job_id = ses_config['batch_job_2_id']

        # 1. Check if the specified EFS folder exists
        if not os.path.exists(render_output_path):
            raise FileNotFoundError(f"EFS folder not found: {render_output_path}")
        
        # 2. Comprimir a .zip la carpeta /output dentro de /output (output.zip)
        output_zip_path, zip_size = output_to_zip(render_output_path)
        print(f"output.zip created path: {output_zip_path}")
        print(f"Size of output.zip: {zip_size} bytes")
        
        # 3. Crear thumbnail de la primera imagen que haya en output, guardarlo en la misma ruta de files (efs project path env) como: _thumbnail.png
        thumbnail_path = generate_thumbnail(render_output_path, thumbnail_output_path)
        print(f"Thumbnail created path: {thumbnail_path}")

        # 4. Upload the /output folder and output.zip to the specified S3 bucket
        response = upload_to_s3(render_output_path, output_zip_path, thumbnail_path)
        print(f"Upload to S3 response: {response}")

        """
        Parsed JSON SES: {'ses': {'ses_active': True, 'render_details': {'project_name': 'Project_5', 'resolution': '1920x1080', 'scene_name': 'Scene', 'layer_name': 'Layer1', 'camera_name': 'Camera1', 'samples': '200', 'engine': 'CYCLES', 'render_type': 'Still'}, 'ses_config': {'region': 'us-east-1', 'source_email': 'rejdev24@gmail.com', 'destination_email': 'rejdev24@gmail.com', 'render_ok_template_name': 'RenderCompletedTemplate', "batch_job_2_id": "45557eab-576d-41ff-a2ba-2c357ab5037e"}}}
        """

        print(f"SES Active: {ses_active}")
        print(f"Render Details: {render_details}")
        print(f"SES Config: {ses_config}")

        if not ses_active:
            print("SES is not active, skipping email sending")
            exit(0)
        else:
            print("SES is active, sending email")  

            # 5. Crear url presignada de thumbnail (para ses template) y de output.zip (para ses template)
            thumbnail_presigned_url, output_zip_presigned_url = generate_presigned_urls(region)
            print(f"Thumbnail presigned url: {thumbnail_presigned_url}")
            print(f"Output.zip presigned url: {output_zip_presigned_url}")

            # 6. Get aws batch job 2 details (ec2 type, instance type, vcpus, memory, and job start , end time, etc.)
            runtime, status = get_batch_job_info(job_id, region, render_details)

            print(f"Runtime minutes: {runtime}")
            
            # 7. Ses logic to send email with the presigned urls (template with the urls)
            response = send_render_ok_email(thumbnail_presigned_url, output_zip_presigned_url, ses_config, render_details, zip_size, runtime)
            print(f"SES response: {response}")


        # 8. Clean up the EFS folder
        clean_up_project_folder_efs(efs_path, bucket_key)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Sending error email to user")
        runtime, status = get_batch_job_info(job_id, region, render_details)
        print(f"Runtime: {runtime}")
        print(f"Status: {status}")

        statusReason = status['reason']
        print(f"Status Reason: {statusReason}")
        logStreamName = status['log_stream_name']
        print(f"Log Stream Name: {logStreamName}")

        # Clean up the EFS folder
        clean_up_project_folder_efs(efs_path, bucket_key)

        if not ses_active:
            print("SES is not active, skipping email sending")
            exit(0)
        else:
        # enviar email con error
            response = send_render_error_email(ses_config, render_details, runtime, status)
            print(f"SES response: {response}")

        exit(1)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
