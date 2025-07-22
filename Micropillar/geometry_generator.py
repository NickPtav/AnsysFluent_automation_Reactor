import os
import subprocess
import time

# attention!
# make sure to use the right Ansys version
# In this code "v232", but you can check your version going to "C:\\Program Files\\ANSYS Inc\\ANSYS Student"

def run_spaceclaim_script(script_path):
    command = f'cd "C:\\Program Files\\ANSYS Inc\\ANSYS Student\\v251\\scdm" && SpaceClaim.exe /RunScript="{script_path}" /Headless=True /Splash=False /Welcome=False /ExitAfterScript=True'
    subprocess.run(command, shell=True)

def get_script_paths(folder_path):
    script_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                script_paths.append(os.path.join(root, file))
    return script_paths

# Pasta onde os scripts estão localizados
scripts_folder = r'YOURDIRECTORY'

# Obter os caminhos dos scripts na pasta
script_paths = get_script_paths(scripts_folder)

# Executar cada script na lista
for script_path in script_paths:
    run_spaceclaim_script(script_path)
    time.sleep(5)  # Aguardar 5 segundos entre os scripts
