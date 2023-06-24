from subprocess import run
import os

# set path
webui_path = "/workspace/stable-diffusion-webui/"
zip_file_path = os.path.join(webui_path, "outputs.zip")  

# function to run bash command
def run_cmd(cmd, cwd=None):
    run(cmd, cwd=cwd, shell=True, check=True)

if os.path.exists(zip_file_path):
    os.remove(zip_file_path)
    
# send outputs folder
run_cmd("runpodctl send outputs", cwd=webui_path)