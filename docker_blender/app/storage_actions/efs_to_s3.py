import os
import boto3
import shutil

def upload_to_s3(local_path, bucket_name, s3_path, s3):
    try:
        s3.upload_file(local_path, bucket_name, s3_path)
        print(f"Uploaded {local_path} to S3 at {s3_path}")
    except FileNotFoundError:
        print(f"Error: File not found - {local_path}")
    except Exception as e:
        print(f"Error uploading {local_path} to S3: {e}")

def main():
    try:
        # Ensure required environment variables are present
        required_env_vars = ['BUCKET_NAME', 'BUCKET_KEY', 'EFS_BLENDER_FOLDER_PATH']
        for env_var in required_env_vars:
            if env_var not in os.environ:
                raise ValueError(f"Missing environment variable: {env_var}")

        bucket_name = os.environ['BUCKET_NAME']
        bucket_key = os.environ['BUCKET_KEY']
        efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']
        print(f"EFS path: {efs_path}")
        render_output_path = os.path.join(efs_path, bucket_key, 'output')
        print(f"Render output path: {render_output_path}")

        print("Cleaning up EFS folder")

        # Check if the specified EFS folder exists
        if not os.path.exists(render_output_path):
            raise FileNotFoundError(f"EFS folder not found: {render_output_path}")

        # Upload to S3
        s3 = boto3.client('s3')
        for root, dirs, files in os.walk(render_output_path):
            for file in files:
                local_path = os.path.join(root, file)
                s3_path = os.path.join(bucket_key, 'output', os.path.relpath(local_path, render_output_path))
                upload_to_s3(local_path, bucket_name, s3_path, s3)
                print("Render output uploaded to S3")

        # Clean /mnt/projects/project_name folder
        try:
            shutil.rmtree(os.path.join(efs_path, bucket_key))
            print("EFS folder cleaned up")
        except FileNotFoundError:
            print("Error: EFS folder not found")
        except Exception as e:
            print(f"Error cleaning up EFS folder: {e}")

    except ValueError as ve:
        print(f"Error: {ve}")
    except FileNotFoundError as fnfe:
        print(f"Error: {fnfe}")
    except Exception as e:
        print(f"Unhandled error: {e}")

if __name__ == "__main__":
    main()