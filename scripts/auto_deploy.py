#######################################
#Install everything you want in one script kind of...
#######################################
# Disclaimer: I am not proficient in writing python or knowing what to implement how. I tried my best to get it to working with examples and ChatGPT.
# If you use this to make a better one, please let me know. I'm shure there are better ways then this. But for now it works...

#######################################
#CHECK FOR PACKAGES AND INSTALL IF NOT AVAILABLE
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
#VARIABLES
#######################################

#### SET YOUR ROOT HERE 
root = "/workspace"

#### SET YOUR WEBUI-USER FLAGS --force-enable-xformers --xformers --no-half --no-half-vae --opt-split-attention --opt-channelslast --opt-sdp-no-mem-attention
flags = "--opt-sdp-attention --port 3001 --listen --enable-insecure-extension-access --api --theme=dark"

#### SET EXTENSIONS TO INSTALL
extension_list = [
                    "https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper",
                    "https://jihulab.com/hunter0725/a1111-sd-webui-tagcomplete",
                    "https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111",
                    "https://github.com/ArtVentureX/sd-webui-agent-scheduler",
                    "https://github.com/kohya-ss/sd-webui-additional-networks",
                    "https://github.com/camenduru/openpose-editor",
                    "https://github.com/zanllp/sd-webui-infinite-image-browsing",
                    "https://github.com/hnmr293/posex",
                    "https://github.com/yankooliveira/sd-webui-photopea-embed",
                    "https://github.com/civitai/sd_civitai_extension",
                    "https://jihulab.com/hunter0725/stable-diffusion-webui-wd14-tagger",
                    "https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards"
                ]

#### SET CHECKPOINT MODELS TO DOWNLOAD
checkpoint_models = [
                        "https://civitai.com/api/download/models/77276"
                    ]

### SET LORA MODELS TO DOWNLOAD
lora_models = [
                "https://civitai.com/api/download/models/96573",
                "https://civitai.com/api/download/models/87153", 

            ]

#### SET VAE TO DOWNLOAD
vae_models = [
                "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt",
                "https://civitai.com/api/download/models/88156"
            ]

#######################################
#SWITCHES
#######################################
# s
init_packages = True
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
#INIT PACKAGES INSTALLATION
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
#DOWNLOAD FUNCTIONS
#######################################

# download function from google drive
def gdown_func(id, output):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, output, quiet=False)

# download function from url
def download_files(urls, output_path):
    for url in urls:
        filename = url.split('/')[-1]  # 获取url中的文件名
        command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -o {filename} {url} -d {output_path}"
        result = os.system(command)
        if result == 0:
            print(f"{url} downloaded successfully!")
        else:
            print(f"An error occurred while downloading {url}.")

#######################################
#DOWNLOAD MISC FILES FROM GOOGLE DRIVE
#######################################

if download_styles:
    # import styles.csv file from google drive
    def styles_down():
        if os.path.exists(f'{root}/stable-diffusion-webui/styles.csv'):
            os.remove(f'{root}/stable-diffusion-webui/styles.csv')
        gdown_func("19n4B46ey0egTwzC27dqE0A0PkHN58Uc_", f"{root}/stable-diffusion-webui/styles.csv")
    print("========== Downloading styles.csv file from Google Drive...========== \n")
    styles_down()

#######################################
#EMBEDDING MODELS
#######################################

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
#CHECKPOINT MODELS
#######################################

if download_checkpoints:
    checkpoint_model_path = f"{root}/stable-diffusion-webui/models/Stable-diffusion"
    print("========== Downloading models...========== \n")
    download_files(checkpoint_models, checkpoint_model_path)

#######################################
#VAE
#######################################

if download_vae_models:
    vae_path = f"{root}/stable-diffusion-webui/models/VAE"
    print("========== Downloading VAEs From...========== \n")
    download_files(vae_models, vae_path)

#######################################
#LORAS
#######################################

if download_lora:
    lora_path = f"{root}/stable-diffusion-webui/models/Lora"
    print("========== Downloading LORAs...========== \n")
    download_files(lora_models, lora_path)

#######################################
#EXTENSIONS
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

#######################################
# CONTROLNET with all models
# The Controlnet Application didnt work like above but the Runpod Template Fast SD had a better implementation then mine so i used that
# Future improvement would be to get all extension installation in this format.
# This uses the model list in the TheLastBen colab notebook

if download_controlnet:
    extensions_path = f"{root}/stable-diffusion-webui/extensions"
    models_path = f"{root}/stable-diffusion-webui/extensions/sd-webui-controlnet/models"
    cn_models_txt = f"{root}/CN_models.txt"
    cn_models_v2_txt = f"{root}/CN_models_v2.txt"

    def wget_file(url, dest_path):
        subprocess.run(['wget', '-q', '-O', dest_path, url], check=True)

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

    print("========== Downloading models...========== \n")
    clone_or_pull_repo('https://github.com/Mikubill/sd-webui-controlnet.git', f"{extensions_path}/sd-webui-controlnet")

    for filename in os.listdir(models_path):
        if "_sd14v1" in filename:
            renamed = re.sub("_sd14v1", "-fp16", filename)
            os.rename(os.path.join(models_path, filename), os.path.join(models_path, renamed))

    wget_file('https://github.com/TheLastBen/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/CN_models.txt', cn_models_txt)
    wget_file('https://github.com/TheLastBen/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/CN_models_v2.txt', cn_models_v2_txt)

    with open(cn_models_txt, 'r') as f:
        model_links = f.read().splitlines()
    with open(cn_models_v2_txt, 'r') as d:
        model_links_v2 = d.read().splitlines()

    for link in model_links + model_links_v2:
        download(link, models_path)

    subprocess.run(['rm', cn_models_txt, cn_models_v2_txt], check=True)

    config_names=[os.path.basename(url).split('.')[0]+'.yaml' for url in model_links_v2]
    for name in config_names:
        copy_files(f"{models_path}/cldm_v21.yaml", f"{models_path}/{name}")


#######################################
#other stuff
#######################################
# # change working directory
# os.chdir(f"{root}/stable-diffusion-webui")
# # reset git repository
# result = os.system("git reset --hard")
# if result == 0:
#     print("Git repository reset successfully!")
# else:
#     print("An error occurred while resetting Git repository.")

# # install controlnet requirements In another script it was called at this point after the reset, so I left it here.
# # change working directory
# os.chdir(f"{root}/stable-diffusion-webui/extensions/sd-webui-controlnet")

# result = os.system("pip install -r requirements.txt")
# if result == 0:
#     print("Requirements.txt installed successfully!")
# else:
#     print("An error occurred while installing the requirements.txt")

# # change working directory to stable-diffusion-webui
# os.chdir(f"{root}/stable-diffusion-webui/")

if edit_relauncher:
    # modify relauncher.py file
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

if edit_webui_user:
    # modify webui-user.sh file
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


# took this from the google colab code I used before. No idea why it changes that line and it doesn't work. so off it goes... (I know I'm a mess)
# Replace `prepare_environment()` with `prepare_environment():`
#os.system(f"""sed -i -e '/prepare_environment():/a\    os.system(f\\"sed -i -e ''\\"s/dict()))/dict())).cuda()/g\\"'' {root}/stable-diffusion-#webui/repositories/stable-diffusion-stability-ai/ldm/util.py" {root}/stable-diffusion-webui/launch.py""")
#os.system(f"""cd {root}/stable-diffusion-webui/repositories/k-diffusion; git config core.filemode false""")

#I cant get this to work, so I'm uploading a custom webur-user.sh for now and start using relauncher.py included in the sd template

#args = "--port 3010 --gradio-img2img-tool color-sketch -- share --listen --enable-insecure-extension-access --gradio-queue --xformers"
#SET USERNAME AND PASSWORD
#username = "Lennart"
#password = "C"
#if username and password:
#    args += f" --gradio-auth {username}:{password} "
#cmd = f"python {root}/stable-diffusion-webui/launch.py {args}"
#result = os.system(cmd)

# make a1111 use the newest torch version, found this online...
# call('pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118', shell=True)

# kill port 3000
os.system("fuser -k 3000/tcp")
print("========== Port 3000 killed...========== \n")

print("All done!")