#@title ##初始化常量与挂载谷歌硬盘（只要重启过colab就要再运行一次）

#@markdown 是否挂载谷歌硬盘（推荐）
use_google_drive = True #@param {type:"boolean"}

import os
import shutil
import sys
from google.colab import drive


ROOT_DIR = os.getcwd()    #获取根目录

SD_SCRIPTS_DIR = os.path.join( ROOT_DIR, "sd-scripts" )    #kohya库克隆路径
WEBUI_DIR = os.path.join( ROOT_DIR, "kohya-config-webui" )   #webui库克隆路径

#TRAIN_DATA_DIR = os.path.join( ROOT_DIR, "Lora", "input" )    #拷贝后训练材料路径
#REG_DATA_DIR = os.path.join( ROOT_DIR, "Lora", "reg" )   #拷贝后正则化材料路径

SD_MODEL_DIR = os.path.join( ROOT_DIR, "Lora", "sd_model" )    #SD模型下载地址
VAE_MODEL_DIR = os.path.join( ROOT_DIR, "Lora", "vae_model" )    #VAE模型下载地址

DEFAULT_COLAB_INPUT_DIR = os.path.normpath("/content/drive/MyDrive/Lora/input")    #默认Colab训练集地址
DEFAULT_COLAB_REG_DIR = os.path.normpath("/content/drive/MyDrive/Lora/reg")    #默认Colab正则化地址
DEFAULT_COLAB_OUPUT_DIR = os.path.normpath("/content/drive/MyDrive/Lora/output")    #默认Colab模型输出地址
DEFAULT_COLAB_WEBUI_SAVE_DIR = os.path.normpath("/content/drive/MyDrive/Lora/kohya_config_webui_save")    #默认Colab保存webui参数文件地址

ACCELERATE_CONFIG_PATH = os.path.join( ROOT_DIR, "accelerate_config.yaml" )   #accelerate库config文件写入地址


#@title ##挂载谷歌硬盘

if use_google_drive:
    if not os.path.exists("/content/drive"):
        drive.mount("/content/drive")

!nvidia-smi

#训练用环境变量
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["BITSANDBYTES_NOWELCOME"] = "1"
os.environ["SAFETENSORS_FAST_GPU"] = "1"




#@title ##克隆github的库、安装依赖
os.chdir( ROOT_DIR )
!git clone https://github.com/kohya-ss/sd-scripts.git {SD_SCRIPTS_DIR}
#@title 克隆我的库
!git clone https://github.com/WSH032/kohya-config-webui.git {WEBUI_DIR}

#安装torch
print(f"torch安装中")
!pip -q install torch torchvision xformers triton
print(f"torch安装完成")

#安装kohya依赖
print(f"kohya依赖安装中")
os.chdir(SD_SCRIPTS_DIR)
!pip -q install -r requirements.txt
os.chdir(ROOT_DIR)
print(f"kohya依赖安装完成")

#安装lion优化器、Dadaption优化器、lycoris
print(f"lion优化器、Dadaption优化器、lycoris安装中")
!pip -q install --upgrade lion-pytorch dadaptation lycoris-lora
print(f"lion优化器、Dadaption优化器、lycoris安装完成")

#安装wandb
print(f"wandb安装中")
!pip -q install wandb
print(f"wandb安装中")

#安装webui依赖
print(f"webui依赖安装中")
os.chdir(WEBUI_DIR)
!pip -q install -r requirements.txt
os.chdir(ROOT_DIR)
print(f"webui依赖安装完成")

#安装功能性依赖
!apt -q install aria2
!pip -q install portpicker


import torch
print("当前torch版本",torch.__version__)
import torchvision
print("当前torchvision版本",torchvision.__version__)
import triton
print("当前triton版本", triton.__version__)

!python -V




#@title ## 下载模型, 可以同时选多个模型下载，到时候是在WebUI里选（原始代码来源于：[Linaqruf](https://github.com/Linaqruf/kohya-trainer)）
installModels = []
installv2Models = []

#@markdown **预设底模**

#@markdown SD1.x model
modelName = ""  # @param ["", "Animefull-final-pruned.ckpt", "Anything-v3-1.safetensors", "AnyLoRA.safetensors", "AnimePastelDream.safetensors", "Chillout-mix.safetensors", "OpenJourney-v4.ckpt", "Stable-Diffusion-v1-5.safetensors"]
#@markdown SD2.x model `这些为SD2.x模型，训练时请开启v2选项`
v2ModelName = ""  # @param ["", "stable-diffusion-2-1-base.safetensors", "stable-diffusion-2-1-768v.safetensors", "plat-diffusion-v1-3-1.safetensors", "replicant-v1.safetensors", "illuminati-diffusion-v1-0.safetensors", "illuminati-diffusion-v1-1.safetensors", "waifu-diffusion-1-4-anime-e2.ckpt", "waifu-diffusion-1-5-e2.safetensors", "waifu-diffusion-1-5-e2-aesthetic.safetensors"]

#@markdown **自定义模型（不能超过5G）URL例如**`https://huggingface.co/a1079602570/animefull-final-pruned/resolve/main/novelailatest-pruned.ckpt`

base_model_url = "" #@param {type:"string"}

#@markdown **或者自定义模型（不能超过5G）路径例如**`/content/drive/MyDrive/Lora/model/your_model.ckpt`

base_model_self_path = "/content/drive/MyDrive/Lora/sd_model/v1-5-pruned-emaonly.safetensors" #@param {type:"string"}


def get_sd_model():
    modelUrl = [
        "",
        "https://huggingface.co/Linaqruf/personal-backup/resolve/main/models/animefull-final-pruned.ckpt",
        "https://huggingface.co/cag/anything-v3-1/resolve/main/anything-v3-1.safetensors",
        "https://huggingface.co/Lykon/AnyLoRA/resolve/main/AnyLoRA_noVae_fp16.safetensors",
        "https://huggingface.co/Lykon/AnimePastelDream/resolve/main/AnimePastelDream_Soft_noVae_fp16.safetensors",
        "https://huggingface.co/Linaqruf/stolen/resolve/main/pruned-models/chillout_mix-pruned.safetensors",
        "https://huggingface.co/prompthero/openjourney-v4/resolve/main/openjourney-v4.ckpt",
        "https://huggingface.co/Linaqruf/stolen/resolve/main/pruned-models/stable_diffusion_1_5-pruned.safetensors",
    ]
    modelList = [
        "",
        "Animefull-final-pruned.ckpt",
        "Anything-v3-1.safetensors",
        "AnyLoRA.safetensors",
        "AnimePastelDream.safetensors",
        "Chillout-mix.safetensors",
        "OpenJourney-v4.ckpt",
        "Stable-Diffusion-v1-5.safetensors",
    ]
    v2ModelUrl = [
        "",
        "https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.safetensors",
        "https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.safetensors",
        "https://huggingface.co/p1atdev/pd-archive/resolve/main/plat-v1-3-1.safetensors",
        "https://huggingface.co/gsdf/Replicant-V1.0/resolve/main/Replicant-V1.0.safetensors",
        "https://huggingface.co/IlluminatiAI/Illuminati_Diffusion_v1.0/resolve/main/illuminati_diffusion_v1.0.safetensors",
        "https://huggingface.co/4eJIoBek/Illuminati-Diffusion-v1-1/resolve/main/illuminatiDiffusionV1_v11.safetensors",
        "https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/wd-1-4-anime_e2.ckpt",
        "https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-fp32.safetensors",
        "https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-aesthetic-fp32.safetensors",
    ]
    v2ModelList = [
        "",
        "stable-diffusion-2-1-base.safetensors",
        "stable-diffusion-2-1-768v.safetensors",
        "plat-diffusion-v1-3-1.safetensors",
        "replicant-v1.safetensors",
        "illuminati-diffusion-v1-0.safetensors",
        "illuminati-diffusion-v1-1.safetensors",
        "waifu-diffusion-1-4-anime-e2.ckpt",
        "waifu-diffusion-1-5-e2.safetensors",
        "waifu-diffusion-1-5-e2-aesthetic.safetensors",
    ]
    if modelName:
        installModels.append((modelName, modelUrl[modelList.index(modelName)]))
    if v2ModelName:
        installv2Models.append((v2ModelName, v2ModelUrl[v2ModelList.index(v2ModelName)]))


    #下载模型
    def install(checkpoint_name, url):
        hf_token = "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"
        user_header = f'"Authorization: Bearer {hf_token}"'
        print(checkpoint_name)
        print(url)
        !aria2c --console-log-level=error --summary-interval=10 --header={user_header} -c -x 16 -k 1M -s 16 -d {SD_MODEL_DIR} -o {checkpoint_name} {url}
    def install_checkpoint():
        for model in installModels:
            install(model[0], model[1])
        for v2model in installv2Models:
            install(v2model[0], v2model[1])

    #下载预设模型
    install_checkpoint()

    #自定义链接不留空，则尝试下载
    if base_model_url:
        #!aria2c --content-disposition-default-utf8=true --console-log-level=error --summary-interval=10 -c -x 16 -k 1M -s 16 -d {SD_MODEL_DIR} {base_model_url}
        !wget {base_model_url} -P {SD_MODEL_DIR} -N

    #自定义路径不留空，则尝试拷贝
    if base_model_self_path:
        try:
            base_model_copy_path = os.path.join( SD_MODEL_DIR, os.path.basename(base_model_self_path) )
            shutil.copyfile(base_model_self_path, base_model_copy_path)
            print(f"拷贝自定义底模成功, {base_model_self_path}被拷贝至{base_model_copy_path}")
        except Exception as e:
            print(f"拷贝自定义底模时发生错误， Error: {e}")

get_sd_model()


#@markdown **(可选)选择一个Vae下载**`"animevae.pt", "kl-f8-anime.ckpt", "vae-ft-mse-840000-ema-pruned.ckpt"`

vaeName = ""  # @param ["", "anime.vae.pt", "waifudiffusion.vae.pt", "stablediffusion.vae.pt"]

def get_vae_model():

    installVae = []

    vaeUrl = [
        "",
        "https://huggingface.co/Linaqruf/personal-backup/resolve/main/vae/animevae.pt",
        "https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime.ckpt",
        "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.ckpt",
    ]
    vaeList = ["", "anime.vae.pt", "waifudiffusion.vae.pt", "stablediffusion.vae.pt"]

    installVae.append((vaeName, vaeUrl[vaeList.index(vaeName)]))

    #开始下载
    def install(vae_name, url):
        hf_token = "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"
        user_header = f'"Authorization: Bearer {hf_token}"'
        print(vae_name)
        print(url)
        !aria2c --console-log-level=error --allow-overwrite --summary-interval=10 --header={user_header} -c -x 16 -k 1M -s 16 -d {VAE_MODEL_DIR} -o {vae_name} "{url}"

    def install_vae():
        if vaeName:
            for vae in installVae:
                install(vae[0], vae[1])
        else:
            pass
    install_vae()

get_vae_model()





#@title ##启动WebUI来设置参数

#@markdown - 在谷歌硬盘的`/content/drive/MyDrive/Lora/kohya_config_webui_save`会生成一个`colab.toml`，在WebUI里读取它，会帮你完成默认参数设置。
#@markdown  - 读取的时候会提示参数找不到，这是正常的
#@markdown - 设置好参数后可以保存`（默认会保存到你的谷歌硬盘）`，以后读取你保存的配置文件就行
#@markdown  - 保存toml配置文件时候不要用`colab.toml`这个名字，会被覆盖掉

#@markdown - 在colab里要开`lowram`，不然很多模型载入不了，读取`colab.toml`的时候会自动帮你开启

#@markdown ---

#@markdown 是否在colab里打开webui`不勾选就输出一个链接，点击后在另一个网页操作，反正我喜欢不勾选`
in_colab = False #@param {type:"boolean"}

#@markdown 是否使用gradio的远程分享及队列功能
use_queue = False #@param {type:"boolean"}

#生成一个colab默认toml文件
def creat_save_toml(save_dir):
    """生成适用于Colab的webui参数保存文件colab.toml"""
    import toml
    #写入路径
    other={"write_files_dir":SD_SCRIPTS_DIR}
    #材料、模型、输出路径
    param={
        "train_data_dir":DEFAULT_COLAB_INPUT_DIR,
        "reg_data_dir":DEFAULT_COLAB_REG_DIR,
        "base_model_dir":SD_MODEL_DIR,
        "vae_model_dir":VAE_MODEL_DIR,
        "output_dir":DEFAULT_COLAB_OUPUT_DIR,
        "lowram":True,
    }

    save_dict = {"other":other, "param":param}
    #写入文件
    save_name = "colab.toml"
    save_path = os.path.join( save_dir, save_name )
    os.makedirs(save_dir, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write( toml.dumps(save_dict) )

creat_save_toml(DEFAULT_COLAB_WEBUI_SAVE_DIR)

#导入并生成demo
launch_param = [f"--save_dir={DEFAULT_COLAB_WEBUI_SAVE_DIR}",
        f"--save_name=kohya_config_webui_save.toml",
        f"--read_dir={DEFAULT_COLAB_WEBUI_SAVE_DIR}"
]
os.chdir( os.path.join(WEBUI_DIR, "module") )
from kohya_config_webui import create_demo
os.chdir(ROOT_DIR)
demo = create_demo(launch_param)

#找一个空闲端口
import portpicker
port = portpicker.pick_unused_port()
#启动
if not use_queue:
    demo.launch(server_port=port, inbrowser=False, inline=False)
    #暴露端口
    from google.colab import output
    output.serve_kernel_port_as_window(port)
    #是否在Colab里打开
    if in_colab:
        output.serve_kernel_port_as_iframe(port)
else:
    demo.queue().launch(server_port=port, inline=in_colab)




#@title ##启动WebUI来设置参数

#@markdown - 在谷歌硬盘的`/content/drive/MyDrive/Lora/kohya_config_webui_save`会生成一个`colab.toml`，在WebUI里读取它，会帮你完成默认参数设置。
#@markdown  - 读取的时候会提示参数找不到，这是正常的
#@markdown - 设置好参数后可以保存`（默认会保存到你的谷歌硬盘）`，以后读取你保存的配置文件就行
#@markdown  - 保存toml配置文件时候不要用`colab.toml`这个名字，会被覆盖掉

#@markdown - 在colab里要开`lowram`，不然很多模型载入不了，读取`colab.toml`的时候会自动帮你开启

#@markdown ---

#@markdown 是否在colab里打开webui`不勾选就输出一个链接，点击后在另一个网页操作，反正我喜欢不勾选`
in_colab = False #@param {type:"boolean"}

#@markdown 是否使用gradio的远程分享及队列功能
use_queue = False #@param {type:"boolean"}

#生成一个colab默认toml文件
def creat_save_toml(save_dir):
    """生成适用于Colab的webui参数保存文件colab.toml"""
    import toml
    #写入路径
    other={"write_files_dir":SD_SCRIPTS_DIR}
    #材料、模型、输出路径
    param={
        "train_data_dir":DEFAULT_COLAB_INPUT_DIR,
        "reg_data_dir":DEFAULT_COLAB_REG_DIR,
        "base_model_dir":SD_MODEL_DIR,
        "vae_model_dir":VAE_MODEL_DIR,
        "output_dir":DEFAULT_COLAB_OUPUT_DIR,
        "lowram":True,
    }

    save_dict = {"other":other, "param":param}
    #写入文件
    save_name = "colab.toml"
    save_path = os.path.join( save_dir, save_name )
    os.makedirs(save_dir, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write( toml.dumps(save_dict) )

creat_save_toml(DEFAULT_COLAB_WEBUI_SAVE_DIR)

#导入并生成demo
launch_param = [f"--save_dir={DEFAULT_COLAB_WEBUI_SAVE_DIR}",
        f"--save_name=kohya_config_webui_save.toml",
        f"--read_dir={DEFAULT_COLAB_WEBUI_SAVE_DIR}"
]
os.chdir( os.path.join(WEBUI_DIR, "module") )
from kohya_config_webui import create_demo
os.chdir(ROOT_DIR)
demo = create_demo(launch_param)

#找一个空闲端口
import portpicker
port = portpicker.pick_unused_port()
#启动
if not use_queue:
    demo.launch(server_port=port, inbrowser=False, inline=False)
    #暴露端口
    from google.colab import output
    output.serve_kernel_port_as_window(port)
    #是否在Colab里打开
    if in_colab:
        output.serve_kernel_port_as_iframe(port)
else:
    demo.queue().launch(server_port=port, inline=in_colab)





#@title linaqfuf优化代码

!sed -i "s@cpu@cuda@" /content/sd-scripts/library/model_util.py

import zipfile
def ubuntu_deps(url, name, dst):
    !wget --show-progress {url}
    with zipfile.ZipFile(name, "r") as deps:
        deps.extractall(dst)
    !dpkg -i {dst}/*
    os.remove(name)
    shutil.rmtree(dst)
deps_dir = "/conent/dep"
ubuntu_deps(
    "https://huggingface.co/Linaqruf/fast-repo/resolve/main/deb-libs.zip",
    "deb-libs.zip",
    deps_dir,
)

!apt -y update
!apt install libunwind8-dev

os.environ["LD_PRELOAD"] = "libtcmalloc.so"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["BITSANDBYTES_NOWELCOME"] = "1"
os.environ["SAFETENSORS_FAST_GPU"] = "1"

cuda_path = "/usr/local/cuda-11.8/targets/x86_64-linux/lib/"
ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
os.environ["LD_LIBRARY_PATH"] = f"{ld_library_path}:{cuda_path}"





#@title ##拷贝材料(支持重复训练时选择新的路径)

#@markdown 训练集路径，正则化集路径(正则化留空则不拷贝)

#@markdown `教程默认路径：`

#@markdown `训练集：/content/drive/MyDrive/Lora/input/`

#@markdown `正则化：/content/drive/MyDrive/Lora/reg/`

train_data_dir_self = "/content/drive/MyDrive/Lora/input/blue_archive" #@param {type:'string'}
reg_data_dir_self = "" #@param {type:'string'}


def copy_data_and_reg(data_dir: str, reg_dir: str = ""):
    """
    将材料拷贝至TRAIN_DATA_DIR和REG_DATA_DIR
    拷贝前会删除之前材料
    data_dir为训练集，必填； reg_dir，默认为空，不填则不拷贝
    """
    #训练集路径为空直接退出
    if not data_dir:
        print(f"训练集路径为空")
        return

    #已经存在拷贝材料则删除
    def rm_dir(dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
    rm_dir(TRAIN_DATA_DIR)
    rm_dir(REG_DATA_DIR)

    #拷贝材料
    def cp_dir(from_dir, to_dir, name):
        print(f"拷贝{name}中")
        try:
            shutil.copytree(from_dir, to_dir, dirs_exist_ok=True)
            print(f"{name}拷贝成功, {from_dir}被拷贝至{to_dir}")
        except Exception as e:
            print(f"拷贝{name}时发生错误， Error: {e}")

    cp_dir(data_dir, TRAIN_DATA_DIR, "训练集")
    if reg_dir:
        cp_dir(reg_dir, REG_DATA_DIR, "训练集")
    else:
        print(f"不拷贝正则化")

copy_data_and_reg(train_data_dir_self, reg_data_dir_self)
