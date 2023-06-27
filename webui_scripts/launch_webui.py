import os
import subprocess
from IPython.display import clear_output
from torch.hub import download_url_to_file
from urllib.parse import urlparse

root = "/workspace"
webui_path = os.path.join(root, "stable-diffusion-webui")

def is_package_installed(package):
    try:
        subprocess.check_call(["dpkg", "-s", package], stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    return True

# function to run bash command
def run_cmd(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

# 列出需要检查的库
libraries = ["libcudnn8=8.9.2.26-1+cuda11.8", "libcudnn8-dev=8.9.2.26-1+cuda11.8"]

# 检查每个库是否已经安装
for lib in libraries:
    if not is_package_installed(lib):
        print(f"Installing {lib}...")
        subprocess.run(["apt", "install", "-y", lib, "--allow-change-held-packages"], check=True)

# kill_port_if_occupied(3000)
# launch webui
run_cmd("python relauncher.py", cwd=webui_path)