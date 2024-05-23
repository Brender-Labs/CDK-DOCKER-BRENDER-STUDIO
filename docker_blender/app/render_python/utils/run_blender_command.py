import sys
import subprocess
import threading
from utils.blender_logs import print_stdout, print_stderr

def run_blender_command(env_vars):
    blender_command = [
        env_vars['blender_executable_path'],
        '-b',
        env_vars['blender_file_path'],
        '-P',
        env_vars['user_main_script_path'],
    ]
    print("Blender command:", ' '.join(blender_command))
    
    process = subprocess.Popen(blender_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print_blender_logs = threading.Thread(target=print_stdout, args=(process,))
    print_error_logs = threading.Thread(target=print_stderr, args=(process,))
    
    print_blender_logs.start()
    print_error_logs.start()

    print_blender_logs.join()
    print_error_logs.join()

    process.stdout.close()
    process.stderr.close()

    rc = process.poll()
    if rc != 0:
        print("Error: Blender command failed with exit code", rc)
        sys.exit(1)