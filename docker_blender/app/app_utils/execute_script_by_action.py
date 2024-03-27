import json
import subprocess

def execute_script_by_action(data, script_path, job_action):

    if script_path is None:
        print(f"Unsupported action: {job_action}")
        return

    if job_action == 'render':
        subprocess.run(['python3', script_path, json.dumps(data)])
    else:
        subprocess.run(['python3', script_path])