#######################################
# Install everything you want in one script kind of...
#######################################
# Disclaimer: I am not proficient in writing python or knowing what to implement how. I tried my best to get it to working with examples and ChatGPT.
# If you use this to make a better one, please let me know. I'm shure there are better ways then this. But for now it works...

#######################################
# CHECK FOR PACKAGES AND INSTALL IF NOT AVAILABLE
#######################################

import importlib
import subprocess
import sys

REQUIRED_PACKAGES = [
    'os', 
    'shutil', 
    'IPython', 
    'subprocess', 
    'time', 
    'ipywidgets', 
    'requests', 
    'sys', 
    'fileinput', 
    'torch', 
    'urllib', 
    're', 
    'zipfile'
]

for package in REQUIRED_PACKAGES:
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package])



# these imports are partially taken from the script use in the fast-sd template from runpod bcs I implemented a small portion of their code. 

import os
import shutil
from IPython.display import clear_output
from subprocess import call, getoutput, Popen, run
import time
import ipywidgets as widgets
import requests
import sys
import fileinput
from torch.hub import download_url_to_file
from urllib.parse import urlparse
import re
import zipfile


#######################################
# VARIABLES
#######################################

#### SET YOUR ROOT HERE 
root = "/workspace"

#### SET YOUR WEBUI-USER FLAGS --force-enable-xformers --xformers --no-half --no-half-vae --opt-split-attention --opt-channelslast --opt-sdp-no-mem-attention
flags = "--opt-sdp-attention --port 3001 --listen --enable-insecure-extension-access --api --theme=dark"

#### SET EXTENSIONS
extension_list = [
                    "https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper",
                    "https://jihulab.com/hunter0725/a1111-sd-webui-tagcomplete",
                    "https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111",
                    "https://github.com/ArtVentureX/sd-webui-agent-scheduler",
                    "https://github.com/kohya-ss/sd-webui-additional-networks",
                    "https://github.com/huchenlei/sd-webui-openpose-editor",
                    "https://github.com/zanllp/sd-webui-infinite-image-browsing",
                    "https://github.com/hnmr293/posex",
                    "https://github.com/yankooliveira/sd-webui-photopea-embed",
                    "https://github.com/civitai/sd_civitai_extension",
                    "https://jihulab.com/hunter0725/stable-diffusion-webui-wd14-tagger",
                    "https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards"
                ]

#### SET CHECKPOINT MODELS
checkpoint_models = [   
                        "https://civitai.com/api/download/models/77276", # perfect world v4
                        "https://civitai.com/api/download/models/79290", # A-Zovya RPG Artist Tools
                    ]

### SET LORA MODELS
lora_models = [
                "https://civitai.com/api/download/models/96573", # 3DMM
                "https://civitai.com/api/download/models/87153", # more_details

            ]

#### SET VAE
vae_models = [
                "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt",
                "https://civitai.com/api/download/models/88156" # ClearVAE
            ]

### SET CONTROLNET MODELS
controlnet_models = [
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.pth"
                    ]

#######################################
# SWITCHES
#######################################

init_packages = True
force_update_webui = False
download_checkpoints = True
download_lora = True
download_vae_models = True
download_embedding_models = True
download_extensions = True
download_controlnet = True
download_styles = True
edit_relauncher = True
edit_webui_user = True

#######################################
# INIT PACKAGES INSTALLATION
#######################################

if init_packages:
    # install lsof
    os.system("apt-get install lsof")

    try:
        os.system("pip install gdown")
        print("gdown successfully installed!")
    except Exception as e:
        print("An error occurred while installing gdown:", e)
        
    import gdown

    result = os.system("apt-get update")
    if result == 0:
        print("Package list updated successfully!")
    else:
        print("An error occurred while updating package list.")

    # install git
    result = os.system("apt-get install -y git")
    if result == 0:
        print("git installed successfully!")
    else:
        print("An error occurred while installing git.")

    #install aria2c
    result = os.system("apt-get install -y aria2")
    if result == 0:
        print("aria2c installed successfully!")
    else:
        print("An error occurred while installing aria2c.")

    #install runpodctl
    result = os.system("wget --quiet --show-progress https://github.com/Run-Pod/runpodctl/releases/download/v1.9.0/runpodctl-linux-amd -O runpodctl && chmod +x runpodctl && cp runpodctl /usr/bin/runpodctl")
    if result == 0:
        print("runpodctl installed successfully!")
    else:
        print("An error occurred while installing runpodctl.")

#######################################
# FUNCTIONS
#######################################

# update git repo function
def update_git_repo(repo_path, force_reset=False, update_submodules=False):
    # change working directory
    os.chdir(repo_path)
    
    # reset git repository
    if force_reset:
        result = os.system("git reset --hard")
        if result == 0:
            print(f"Git repository in {repo_path} reset successfully!")
        else:
            print(f"An error occurred while resetting Git repository in {repo_path}.")
    
    # pull latest version
    result = os.system("git pull")
    if result == 0:
        print(f"Git repository in {repo_path} pulled successfully!")
    else:
        print(f"An error occurred while pulling Git repository in {repo_path}.")

    # Check for submodules and update if present
    if update_submodules and os.path.isfile('.gitmodules'):
        result = os.system("git submodule update --init --recursive")
        if result == 0:
            print(f"Submodules in {repo_path} updated successfully!")
        else:
            print(f"An error occurred while updating submodules in {repo_path}.")

# download function from google drive
def gdown_func(id, output):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, output, quiet=False)

# download function from url
def download_files(urls, output_path):
    for url in urls:
        parsed_url = urlparse(url)
        command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {url} -d {output_path}"
        if 'civitai' not in parsed_url.netloc:
            filename = url.split('/')[-1]  # 获取url中的文件名
            command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -o {filename} {url} -d {output_path}"
        result = os.system(command)
        if result == 0:
            print(f"{url} downloaded successfully!")
        else:
            print(f"An error occurred while downloading {url}.")

#######################################
# UPDATE WEBUI REPO
#######################################

# force get latest version of stable-diffusion-webui
if force_update_webui:
    update_git_repo("/path/to/your/repo", force_reset=True, update_submodules=True)

#######################################
# EMBEDDING MODELS
#######################################
# download embedding models as zip file from google drive, then unzip it
if download_embedding_models:
    def embedding_gdown():
        output_path = f"{root}/stable-diffusion-webui/embeddings"  # 下载和解压的路径
        zip_file_path = os.path.join(output_path, 'embeddings.zip')  # 这是在output_path目录下的file.zip
        gdown_func("1-EXxOitLlXq-uRmGcuTFraRPV1pv3qUQ", zip_file_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
        os.remove(zip_file_path)
    print("========== Downloading embedding files from Google Drive...========== \n")
    embedding_gdown()

#######################################
# CHECKPOINT MODELS
#######################################

if download_checkpoints:
    checkpoint_model_path = f"{root}/stable-diffusion-webui/models/Stable-diffusion"
    print("========== Downloading models...========== \n")
    download_files(checkpoint_models, checkpoint_model_path)

#######################################
# VAE
#######################################

if download_vae_models:
    vae_path = f"{root}/stable-diffusion-webui/models/VAE"
    print("========== Downloading VAEs From...========== \n")
    download_files(vae_models, vae_path)

#######################################
# LORAS
#######################################

if download_lora:
    lora_path = f"{root}/stable-diffusion-webui/models/Lora"
    print("========== Downloading LORAs...========== \n")
    download_files(lora_models, lora_path)

#######################################
# EXTENSIONS
#######################################

if download_extensions:
    def download_extensions(extension_list):
        if os.path.exists(f'{root}/stable-diffusion-webui/extensions'):
            shutil.rmtree(f'{root}/stable-diffusion-webui/extensions')
            os.mkdir(f'{root}/stable-diffusion-webui/extensions')
        extensions_path = f"{root}/stable-diffusion-webui/extensions"
        for extension in extension_list:
            print(f"Cloning {extension} into {extensions_path}...")
            command = f"git clone {extension} {os.path.join(extensions_path, os.path.basename(extension).replace('.git', ''))}"
            result = os.system(command)
            if result == 0:
                print(f"{extension} cloned successfully!")
            else:
                print(f"An error occurred while cloning {extension}.")
    print("========== Downloading extensions...========== \n")
    download_extensions(extension_list)

if download_controlnet:
    def cn_model_download():
        # set output paths
        extensions_path = f"{root}/stable-diffusion-webui/extensions"
        cn_models_path = f"{root}/stable-diffusion-webui/extensions/sd-webui-controlnet/models"

        def wget_file(url, dest_path):
            subprocess.run(['wget', '--progress=bar:force', '-q', '-O', dest_path, url], check=True)

        def clone_or_pull_repo(repo_url, dest_path):
            if not os.path.exists(dest_path):
                subprocess.run(['git', 'clone', repo_url, dest_path], check=True)
            else:
                current_dir = os.getcwd()
                os.chdir(dest_path)
                subprocess.run(['git', 'reset', '--hard'], check=True)
                subprocess.run(['git', 'pull'], check=True)
                os.chdir(current_dir)

        def copy_files(source, dest):
            subprocess.run(['cp', source, dest], check=True)

        def download(url, model_dir):
            filename = os.path.basename(urlparse(url).path)
            dest_path = os.path.join(model_dir, filename)
            if not os.path.exists(dest_path):
                print(f"Downloading: {filename}")
                wget_file(url, dest_path)
            else:
                print(f"The model {filename} already exists")

        print("========== Cloning Controlnet Repo...========== \n")
        # clone controlnet extension repo
        clone_or_pull_repo('https://github.com/Mikubill/sd-webui-controlnet.git', f"{extensions_path}/sd-webui-controlnet")

        # rename yaml files if contains _sd14v1
        for filename in os.listdir(cn_models_path):
            if "_sd14v1" in filename:
                renamed = re.sub("_sd14v1", "-fp16", filename)
                os.rename(os.path.join(cn_models_path, filename), os.path.join(cn_models_path, renamed))
        
        print("========== Downloading models...========== \n")
        # download controlnet model from links
        for link in controlnet_models:
            download(link, cn_models_path)
    cn_model_download()

#######################################
# MISC
#######################################

# download styles.csv file from google drive
if download_styles:
    def styles_down():
        if os.path.exists(f'{root}/stable-diffusion-webui/styles.csv'):
            os.remove(f'{root}/stable-diffusion-webui/styles.csv')
        gdown_func("19n4B46ey0egTwzC27dqE0A0PkHN58Uc_", f"{root}/stable-diffusion-webui/styles.csv")
    print("========== Downloading styles.csv file from Google Drive...========== \n")
    styles_down()

# modify relauncher.py file
if edit_relauncher:
    def modify_relauncherfile(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        with open(filename, 'w') as file:
            for line in lines:
                if 'while True:' in line:
                    line = line.replace('while True:', 'while (n<1):')
                file.write(line)
    print("========== Modifying relauncher.py file...========== \n")
    modify_relauncherfile(f'{root}/stable-diffusion-webui/relauncher.py')

# modify webui-user.sh file
if edit_webui_user:
    def modify_webui_userfile(flags):
        filename = f'{root}/stable-diffusion-webui/webui-user.sh'  # 更新为你的文件路径
        with open(filename, "r") as file:
            content = file.read()
        # 将需要替换的字符串定义在这里
        content = content.replace('export COMMANDLINE_ARGS=""', 'export COMMANDLINE_ARGS="{}"'.format(flags))
        with open(filename, "w") as file:
            file.write(content)
    print("========== Modifying webui-user.sh file...========== \n")
    modify_webui_userfile(flags)

#######################################
# UPDATE XFORMERS, CUDA, CUDNN AND TORCH
#######################################

# https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Install-DreamBooth-Extension-On-RunPod.md
# make a1111 use the newest torch version, found this online...
# call('pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118', shell=True)

# kill port 3000
os.system("fuser -k 3000/tcp")
print("========== Port 3000 killed...========== \n")

print("All done!")