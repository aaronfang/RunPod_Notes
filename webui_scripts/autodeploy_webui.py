# AUTOMATIC DEPOLY DATA FOR STABLE DIFFUSION WEBUI TEMPLATE ON RUNPOD

#######################################
# SWITCHES
#######################################

init_packages = True
force_update_webui = True
edit_relauncher = True
download_checkpoints = True
download_lora = True
download_vae_models = True
download_embedding_models = True
download_wildcards = True
download_extensions = True
download_controlnet = True
download_styles = True
update_venv = True
launch_webui = False

#######################################
# CHECK FOR PACKAGES AND INSTALL IF NOT AVAILABLE
#######################################

import importlib
from subprocess import run
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
    'zipfile',
    'pyperclip',
    'tqdm'
]

for package in REQUIRED_PACKAGES:
    try:
        importlib.import_module(package)
    except ImportError:
        run([sys.executable, "-m", "pip", "install", package])


#######################################
# IMPORT MODULES
#######################################

import os
import shutil
import requests
from urllib.parse import urlparse
import re
import zipfile
from tqdm import tqdm

#######################################
# VARIABLES
#######################################

#### SET YOUR ROOT HERE 
root = "/workspace"
webui_path = os.path.join(root, "stable-diffusion-webui")
venv_path = os.path.join(root, "venv")
extensions_path = os.path.join(webui_path, "extensions")
scripts_path = os.path.join(webui_path, "scripts")

#### SET EXTENSIONS
extension_list = [
                    "https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper",
                    "https://github.com/DominikDoom/a1111-sd-webui-tagcomplete",
                    "https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111",
                    "https://github.com/ArtVentureX/sd-webui-agent-scheduler",
                    "https://github.com/kohya-ss/sd-webui-additional-networks",
                    "https://github.com/huchenlei/sd-webui-openpose-editor",
                    "https://github.com/zanllp/sd-webui-infinite-image-browsing",
                    "https://github.com/yankooliveira/sd-webui-photopea-embed",
                    "https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards",
                    "https://github.com/camenduru/stable-diffusion-webui-images-browser",
                    "https://github.com/Bing-su/adetailer",
                    # "https://github.com/civitai/sd_civitai_extension",
                    # "https://jihulab.com/hunter0725/stable-diffusion-webui-wd14-tagger",
                ]

#### SET CHECKPOINT MODELS
checkpoint_models = [   
                        "https://civitai.com/api/download/models/77276", # perfect world v4
                        # "https://civitai.com/api/download/models/94640", # majicMIX realistic
                        # "https://civitai.com/api/download/models/57618", # Counterfeit-V3.0
                        "https://civitai.com/api/download/models/102996", # ToonYou
                        "https://civitai.com/api/download/models/79290", # A-Zovya RPG Artist Tools
                        "https://civitai.com/api/download/models/90854", # 万象熔炉 | Anything V5/Ink
                        "google_drive_id:1CiYnJ5p1l3hX7kTPWb8iCwf2IpPlVNMx", # refslaveV1_v1.safetensors
                        #"google_drive_id:1BdVp4ckGS6cungoka53U5cTYjppHck-2", # 0.6(nijiv5style_v10) + 0.4(perfectWorld_v3Baked).safetensors
                        # "google_drive_id:10tVNyvb2aEWqjo2eviZOPMMcQdGn7jkZ", # 0.6(perfectWorld_v3Baked) + 0.4(Counterfeit-V3.0_fp32).safetensors
                        # "https://OwlMaster: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@huggingface.co/stabilityai/stable-diffusion-xl-base-0.9/resolve/main/sd_xl_base_0.9.safetensors",
                        # "https://OwlMaster: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@huggingface.co/stabilityai/stable-diffusion-xl-refiner-0.9/resolve/main/sd_xl_refiner_0.9.safetensors",
                    ]

### SET LORA MODELS
lora_models = [
                "https://civitai.com/api/download/models/96573", # 3DMM
                "https://civitai.com/api/download/models/87153", # more_details
                # "https://civitai.com/api/download/models/63006", # LowRA
                "https://civitai.com/api/download/models/16576", # epi_noiseoffset
                # "https://civitai.com/api/download/models/90115", # FilmGirl 胶片风 Film Grain LoRA & LoHA
                # "https://civitai.com/api/download/models/102533" # Instant photo 拍立得/Polaroid LoRA & LoHA
            ]

#### SET VAE
vae_models = [
                "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt",
                # "https://civitai.com/api/download/models/88156" # ClearVAE
            ]

### SET CONTROLNET MODELS
controlnet_models = [
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg.pth",
                        # "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.pth",
                        "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.pth"
                    ]

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

# function to run bash command
def run_cmd(cmd, cwd=None):
    run(cmd, cwd=cwd, shell=True, check=True)

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

# replace text in file
def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(old_text, new_text)
    with open(file_path, 'w') as file:
        file.write(content)

# update git repo function
def update_git_repo(repo_path, repo_url=None, force_reset=False, update_submodules=False, branch=None):
    # clone repository if repo_url is provided and repo doesn't exist
    if repo_url and not os.path.exists(repo_path):
        parent_dir = os.path.dirname(repo_path)
        if update_submodules:
            run(['git', 'clone', '--recurse-submodules', repo_url, repo_path], check=True)
        else:
            run(['git', 'clone', repo_url, repo_path], check=True)
        print(f"Git repository cloned from {repo_url} to {repo_path} successfully!")
    elif os.path.exists(repo_path):
        # change working directory
        os.chdir(repo_path)

        # checkout specific branch if provided
        if branch:
            run(["git", "checkout", branch], check=True)
            print(f"Checked out branch {branch} in {repo_path} successfully!")

        # reset git repository if needed
        if force_reset:
            run(["git", "reset", "--hard"], check=True)
            print(f"Git repository in {repo_path} reset successfully!")
        
        # Check for submodules and update if present
        if update_submodules and os.path.isfile('.gitmodules'):
            run(["git", "pull"], check=True)
            run(["git", "submodule", "update", "--init", "--recursive"], check=True)
            print(f"Submodules in {repo_path} updated successfully!")
        else:
            # pull latest version if repo exists
            run(["git", "pull"], check=True)
            print(f"Git repository in {repo_path} pulled successfully!")

# download function from google drive
def gdown_func(id, output):
    run_cmd(f"gdown {id}", cwd=output)

# download function from url
def download_files(urls, output_path):
    for url in urls:
        parsed_url = urlparse(url)
        command = ""

        if 'civitai' in parsed_url.netloc:
            command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {url} -d {output_path}"
        elif 'huggingface' in parsed_url.netloc:
            filename = url.split('/')[-1]  # 获取url中的文件名
            command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -o {filename} {url} -d {output_path}"
        elif 'google_drive_id' in url:
            gdown_func(url.split(':')[-1], output_path)
            continue

        result = os.system(command)
        if result == 0:
            print(f"{url} downloaded successfully!")
        else:
            print(f"An error occurred while downloading {url}.")

# download file from github
def download_file_from_github(repo_owner, repo_name, file_path, save_dir):
    base_url = "https://raw.githubusercontent.com"
    file_url = os.path.join(base_url, repo_owner, repo_name, 'main', file_path)
    
    response = requests.get(file_url)
    
    # make sure that the request was successful
    if response.status_code == 200:
        # make sure the save_dir exists
        os.makedirs(save_dir, exist_ok=True)
        
        with open(os.path.join(save_dir, os.path.basename(file_path)), 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")

def download_with_progress(url, dest_path):
        filename = os.path.basename(urlparse(url).path)
        response = requests.get(url, stream=True)
        total_length = int(response.headers.get('content-length', 0))

        with open(dest_path, "wb") as file, tqdm(
            desc=f"Downloading {filename}", total=total_length, unit="B", unit_scale=True
        ) as progress_bar:
            for data in response.iter_content(chunk_size=4096):
                file.write(data)
                progress_bar.update(len(data))

#######################################
# PRINT CURRENT HARDWARE
#######################################
run_cmd("nvidia-smi")

#######################################
# MODIFY RELAUNCHER.PY
#######################################

if edit_relauncher:
    file_path = os.path.join(webui_path,'relauncher.py')
    old_text = 'while True:'
    new_text = 'while (n<1):'

    replace_text_in_file(file_path, old_text, new_text)

    print("========== relauncher.py modified. Please Restart Pod...========== \n")

#######################################
# UPDATE WEBUI REPO
#######################################

# force get latest version of stable-diffusion-webui
if force_update_webui:
    print("========== Force Updating webui Repo to the Latest...========== \n")
    update_git_repo(webui_path, branch='master', force_reset=True, update_submodules=False)

#######################################
# EMBEDDING MODELS
#######################################
# download embedding models as zip file from google drive, then unzip it
if download_embedding_models:
    def embedding_gdown():
        output_path = f"{root}/stable-diffusion-webui/embeddings"  # 下载和解压的路径
        zip_file_path = os.path.join(output_path, 'embeddings.zip')  # 这是在output_path目录下的file.zip
        gdown_func("1-EXxOitLlXq-uRmGcuTFraRPV1pv3qUQ", output_path)
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

    # download AutoChar to script folder - https://github.com/alexv0iceh/AutoChar
    print("========== Downloading AutoChar Script...========== \n")
    download_file_from_github('alexv0iceh', 'AutoChar', 'AutoChar_v08_release.py', scripts_path)
    download_file_from_github('alexv0iceh', 'AutoChar', 'face_detection_yunet_2022mar.onnx', scripts_path)

if download_controlnet:
    def cn_model_download():
        extensions_path = f"{root}/stable-diffusion-webui/extensions"
        cn_models_path = f"{root}/stable-diffusion-webui/extensions/sd-webui-controlnet/models"

        update_git_repo(f"{extensions_path}/sd-webui-controlnet", repo_url='https://github.com/Mikubill/sd-webui-controlnet.git')

        for filename in os.listdir(cn_models_path):
            if "_sd14v1" in filename:
                renamed = re.sub("_sd14v1", "-fp16", filename)
                os.rename(os.path.join(cn_models_path, filename), os.path.join(cn_models_path, renamed))

        print("========== Downloading models...========== \n")
        for link in controlnet_models:
            filename = os.path.basename(urlparse(link).path)
            dest_path = os.path.join(cn_models_path, filename)
            if not os.path.exists(dest_path):
                print(f"========== {filename} not in path {cn_models_path}, downloading... ========== \n")
                download_with_progress(link, dest_path)
            else:
                print(f"========== The model {filename} already exists ========== \n")

    cn_model_download()

#######################################
# MISC
#######################################

# download wildcards files as zip file from google drive, then unzip it
if download_wildcards:
    def wildcards_gdown():
        output_path = f"{root}/stable-diffusion-webui/extensions/stable-diffusion-webui-wildcards"  # 下载和解压的路径
        # 检查output_path是否存在，不存在则返回并不执行后续工作
        if not os.path.exists(output_path):
            print(f"{output_path} doesn't exist. Skipping copy wildcard resources.")
            return
        zip_file_path = os.path.join(output_path, 'wildcards.zip')  # 这是在output_path目录下的file.zip
        gdown_func("1wzSyB6uOrmcGjD9eue4SPfrZfCX1LQfn", output_path)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
        os.remove(zip_file_path)
    print("========== Downloading wildcards files from Google Drive...========== \n")
    wildcards_gdown()

# download styles.csv file from google drive
if download_styles:
    def styles_down():
        if os.path.exists(f'{root}/stable-diffusion-webui/styles.csv'):
            os.remove(f'{root}/stable-diffusion-webui/styles.csv')
        gdown_func("19n4B46ey0egTwzC27dqE0A0PkHN58Uc_", f"{root}/stable-diffusion-webui/")
    print("========== Downloading styles.csv file from Google Drive...========== \n")
    styles_down()

#######################################
# UPDATE XFORMERS, CUDA, CUDNN AND TORCH
#######################################

if update_venv:
    # pip path in venv
    pip_path = f"{venv_path}/bin/pip"
    
    # install xformers
    run_cmd(f"{pip_path} install xformers==0.0.20")

    # pip install extra modules
    run_cmd(f"{pip_path} install sqlalchemy")
    run_cmd(f"{pip_path} install ultralytics")
    run_cmd(f"{pip_path} install python-dotenv")

    # reinstall torch, torchvision and torchaudio
    run_cmd(f"yes | {pip_path} uninstall torch torchvision torchaudio")
    run_cmd(f"yes | {pip_path} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")

    # 列出需要检查的库
    libraries = ["libcudnn8=8.9.2.26-1+cuda11.8", "libcudnn8-dev=8.9.2.26-1+cuda11.8"]

    # 检查每个库是否已经安装
    for lib in libraries:
        package_name, package_version = lib.split('=')
        
        # 检查当前已安装版本
        result = run(["apt-cache", "policy", package_name], capture_output=True, text=True)
        installed_line = [line for line in result.stdout.split('\n') if 'Installed:' in line][0]
        installed_version = installed_line.split(':')[1].strip()
        
        # 如果未安装或版本不匹配
        if installed_version == '(none)' or installed_version != package_version:
            print(f"Installing {lib}...")
            run(["apt", "install", "-y", lib, "--allow-change-held-packages"], check=True)
        else:
            print(f"{lib} is already installed.")

# replace webui-user.sh
shutil.copy('/workspace/webui-user.sh', '/workspace/stable-diffusion-webui/webui-user.sh')
print("========== webui-user.sh Replaced ==========")

# replace config.json
shutil.copy('/workspace/config.json', '/workspace/stable-diffusion-webui/config.json')
print("========== config.json Replaced ==========")

print("========== All Done! ==========")

if launch_webui:
    # launch webui
    run_cmd("python relauncher.py", cwd=webui_path)