import os
import subprocess

root = "/workspace"
webui_path = os.path.join(root, "stable-diffusion-webui")

# 列出需要检查的库
libraries = ["libcudnn8=8.9.2.26-1+cuda11.8", "libcudnn8-dev=8.9.2.26-1+cuda11.8"]

# 检查每个库是否已经安装
for lib in libraries:
    package_name, package_version = lib.split('=')
    
    # 检查当前已安装版本
    result = subprocess.run(["apt-cache", "policy", package_name], capture_output=True, text=True)
    installed_line = [line for line in result.stdout.split('\n') if 'Installed:' in line][0]
    installed_version = installed_line.split(':')[1].strip()
    
    # 如果未安装或版本不匹配
    if installed_version == '(none)' or installed_version != package_version:
        print(f"Installing {lib}...")
        subprocess.run(["apt", "install", "-y", lib, "--allow-change-held-packages"], check=True)
    else:
        print(f"{lib} is already installed.")

# launch webui
subprocess.run(["./webui.sh", "-f"], cwd=webui_path, check=True)