import sys
import subprocess

def run_blender_command(env_vars):
    blender_command = [
        env_vars['blender_executable_path'],
        '-b',
        env_vars['blender_file_path'],
        '-P',
        env_vars['user_main_script_path'],
    ]
    print("Comando de Blender:", ' '.join(blender_command))
    result = subprocess.run(blender_command, capture_output=True, text=True)
    print("Salida de Blender:", result.stdout)
    print("Errores de Blender:", result.stderr)
    if result.returncode != 0:
        print("Error: El comando de Blender falló.")
        sys.exit(1)