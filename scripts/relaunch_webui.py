from subprocess import run
import os
import shutil

# set path
root = "/workspace"
webui_path = os.path.join(root, "stable-diffusion-webui")

# function to run bash command
def run_cmd(cmd, cwd=None):
    run(cmd, cwd=cwd, shell=True, check=True)

# function to run bash command with return
def run_cmd_return(cmd):
    result = run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

# kill port if occupied
def kill_port_if_occupied(port):
    cmd = f"fuser -k {port}/tcp"
    try:
        return_code, stdout, stderr = run_cmd_return(cmd)
        if stdout:
            print(f"Port {port} is occupied. Killing the process...")
            return_code, stdout, stderr = run_cmd_return(cmd)
            if return_code == 0:
                print(f"Process on port {port} killed successfully.")
            else:
                print(f"Failed to kill the process on port {port}.")
        else:
            print(f"Port {port} is not occupied.")
    except Exception as e:
        print(f"An error occurred while executing the command: {e}")

# kill port 3000 if needed
kill_port_if_occupied(3000)

# replace webui-user.sh
shutil.copy('/workspace/webui-user.sh', '/workspace/stable-diffusion-webui/webui-user.sh')
print("========== webui-user.sh Replaced ==========")

# make sure cuda and cudnn version installed
run_cmd("yes | apt install -y libcudnn8=8.9.2.26-1+cuda11.8 libcudnn8-dev=8.9.2.26-1+cuda11.8 --allow-change-held-packages")

# launch webui
run_cmd("python relauncher.py", cwd=webui_path)