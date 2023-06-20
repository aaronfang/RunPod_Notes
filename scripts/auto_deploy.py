#######################################
#Install everything you want in one script kind of...
#######################################
# Disclaimer: I am not proficient in writing python or knowing what to implement how. I tried my best to get it to working with examples and ChatGPT.
# If you use this to make a better one, please let me know. I'm shure there are better ways then this. But for now it works...

#### SET YOUR ROOT HERE 
root = "/workspace"

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

# flags = "--port 3000 --theme=dark --listen --api --force-enable-xformers --xformers --no-half --no-half-vae --opt-split-attention --opt-channelslast --opt-sdp-no-mem-attention --enable-insecure-extension-access"
flags = "--opt-sdp-attention --port 3001 --listen --enable-insecure-extension-access --api --theme=dark"
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
checkpoint_models = [
                        "https://civitai.com/api/download/models/77276"
                    ]
vae_models = [
                "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt"
            ]


#######################################
#SWITCHES
#######################################
# s
init_packages = True
download_checkpoints = True
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
#DOWNLOAD MISC FILES FROM GOOGLE DRIVE
#######################################

def gdown_func(id, output):
    url = f'https://drive.google.com/uc?id={id}'
    gdown.download(url, output, quiet=False)

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
    def download_models(checkpoint_models):
        models_path = f"{root}/stable-diffusion-webui/models/Stable-diffusion"
        models = checkpoint_models
        for model in models:
            for model in models:
                command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {model} -d {models_path}"
                result = os.system(command)
                if result == 0:
                    print(f"{model} downloaded successfully!")
                else:
                    print(f"An error occurred while downloading {model}.")          
    print("========== Downloading models...========== \n")
    download_models(checkpoint_models)

#######################################
#VAE
#######################################

if download_vae_models:
    def vae_down(vae_models):
        for vae in vae_models:
            filename = vae.split('/')[-1]  # 获取url中的文件名
            filepath = f"{root}/stable-diffusion-webui/models/VAE"
            command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -o {filename} {vae} -d {filepath}"
            result = os.system(command)
            if result == 0:
                print(f"{vae} downloaded successfully!")
            else:
                print(f"An error occurred while downloading {vae}.")
        print("VAE install completed.")
    
print("========== Downloading VAEs...========== \n")
vae_down(vae_models)


#######################################
#LORAS
#######################################


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
    def download(url, model_dir):
        filename = os.path.basename(urlparse(url).path)
        pth = os.path.abspath(os.path.join(model_dir, filename))
        if not os.path.exists(pth):
            print('Downloading: '+os.path.basename(url))
            download_url_to_file(url, pth, hash_prefix=None, progress=True)
        else:
            print(f"The model {filename} already exists")

    wrngv1=False
    os.chdir(f'{root}/stable-diffusion-webui/extensions')
    if not os.path.exists("sd-webui-controlnet"):
        call('git clone https://github.com/Mikubill/sd-webui-controlnet.git', shell=True)
        os.chdir(f'{root}')
    else:
        os.chdir('sd-webui-controlnet')
        call('git reset --hard', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        call('git pull', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        os.chdir(f'{root}')

    mdldir=f"{root}/stable-diffusion-webui/extensions/sd-webui-controlnet/models"
    for filename in os.listdir(mdldir):
        if "_sd14v1" in filename:
            renamed = re.sub("_sd14v1", "-fp16", filename)
            os.rename(os.path.join(mdldir, filename), os.path.join(mdldir, renamed))

    call('wget -q -O CN_models.txt https://github.com/TheLastBen/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/CN_models.txt', shell=True)
    call('wget -q -O CN_models_v2.txt https://github.com/TheLastBen/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/CN_models_v2.txt', shell=True)

    with open("CN_models.txt", 'r') as f:
        mdllnk = f.read().splitlines()
    with open("CN_models_v2.txt", 'r') as d:
        mdllnk_v2 = d.read().splitlines()
    call('rm CN_models.txt CN_models_v2.txt', shell=True)

    cfgnames=[os.path.basename(url).split('.')[0]+'.yaml' for url in mdllnk_v2]
    os.chdir(f'{root}/stable-diffusion-webui/extensions/sd-webui-controlnet/models')
    for name in cfgnames:
        run(['cp', 'cldm_v21.yaml', name])
    os.chdir(f'{root}')

    for lnk in mdllnk:
        download(lnk, mdldir)
    clear_output()

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