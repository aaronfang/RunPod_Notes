#!/bin/bash

# 初始化常量
ROOT_DIR="/workspace"

SD_SCRIPTS_DIR="${ROOT_DIR}/sd-scripts"    # kohya库克隆路径
WEBUI_DIR="${ROOT_DIR}/kohya-config-webui"   # webui库克隆路径

SD_MODEL_DIR="${ROOT_DIR}/Lora/sd_model"    # SD模型下载地址
VAE_MODEL_DIR="${ROOT_DIR}/Lora/vae_model"    # VAE模型下载地址

# 在此根据你的实际路径进行配置
DEFAULT_INPUT_DIR="<Your Input Path>"    # 训练集地址
DEFAULT_REG_DIR="<Your Reg Path>"    # 正则化地址
DEFAULT_OUPUT_DIR="<Your Output Path>"    # 模型输出地址
DEFAULT_WEBUI_SAVE_DIR="<Your Webui Save Path>"    # 保存webui参数文件地址

ACCELERATE_CONFIG_PATH="${ROOT_DIR}/accelerate_config.yaml"   # accelerate库config文件写入地址

# 训练用环境变量
export TF_CPP_MIN_LOG_LEVEL="3"
export BITSANDBYTES_NOWELCOME="1"
export SAFETENSORS_FAST_GPU="1"

# 克隆github的库
cd $ROOT_DIR
git clone https://github.com/kohya-ss/sd-scripts.git $SD_SCRIPTS_DIR
git clone https://github.com/WSH032/kohya-config-webui.git $WEBUI_DIR

# 安装torch
pip install torch torchvision xformers triton

# 安装kohya依赖
cd $SD_SCRIPTS_DIR
pip install -r requirements.txt
cd $ROOT_DIR

# 安装lion优化器、Dadaption优化器、lycoris
pip install --upgrade lion-pytorch dadaptation lycoris-lora

# 安装wandb
pip install wandb

# 安装webui依赖
cd $WEBUI_DIR
pip install -r requirements.txt
cd $ROOT_DIR

# 安装功能性依赖
apt install aria2
pip install portpicker


# SD模型和VAE模型的URL列表
declare -A sd_model_urls=(
    ["Animefull-final-pruned.ckpt"]="https://huggingface.co/Linaqruf/personal-backup/resolve/main/models/animefull-final-pruned.ckpt"
    ["Anything-v3-1.safetensors"]="https://huggingface.co/cag/anything-v3-1/resolve/main/anything-v3-1.safetensors"
    ["AnyLoRA_noVae_fp16.safetensors"]="https://huggingface.co/Lykon/AnyLoRA/resolve/main/AnyLoRA_noVae_fp16.safetensors"
    ["AnimePastelDream_Soft_noVae_fp16.safetensors"]="https://huggingface.co/Lykon/AnimePastelDream/resolve/main/AnimePastelDream_Soft_noVae_fp16.safetensors"
    ["chillout_mix-pruned.safetensors"]="https://huggingface.co/Linaqruf/stolen/resolve/main/pruned-models/chillout_mix-pruned.safetensors"
    ["openjourney-v4.ckpt"]="https://huggingface.co/prompthero/openjourney-v4/resolve/main/openjourney-v4.ckpt"
    ["stable_diffusion_1_5-pruned.safetensors"]="https://huggingface.co/Linaqruf/stolen/resolve/main/pruned-models/stable_diffusion_1_5-pruned.safetensors"
)

declare -A vae_model_urls=(
    ["anime.vae.pt"]="https://huggingface.co/Linaqruf/personal-backup/resolve/main/vae/animevae.pt"
    ["waifudiffusion.vae.pt"]="https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime.ckpt"
    ["plat-v1-3-1.safetensors"]="https://huggingface.co/p1atdev/pd-archive/resolve/main/plat-v1-3-1.safetensors"
    ["Replicant-V1.0.safetensors"]="https://huggingface.co/gsdf/Replicant-V1.0/resolve/main/Replicant-V1.0.safetensors"
    ["illuminati_diffusion_v1.0.safetensors"]="https://huggingface.co/IlluminatiAI/Illuminati_Diffusion_v1.0/resolve/main/illuminati_diffusion_v1.0.safetensors"
    ["illuminatiDiffusionV1_v11.safetensors"]="https://huggingface.co/4eJIoBek/Illuminati-Diffusion-v1-1/resolve/main/illuminatiDiffusionV1_v11.safetensors"
    ["wd-1-4-anime_e2.ckpt"]="https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/wd-1-4-anime_e2.ckpt"
    ["wd-1-5-beta2-fp32.safetensors"]="https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-fp32.safetensors"
    ["wd-1-5-beta2-aesthetic-fp32.safetensors"]="https://huggingface.co/waifu-diffusion/wd-1-5-beta2/resolve/main/checkpoints/wd-1-5-beta2-aesthetic-fp32.safetensors"

)

# 要下载的SD模型和VAE模型的名称
sd_models=("stable_diffusion_1_5-pruned.safetensors" ) # ... 其他模型
vae_models=("anime.vae.pt" "waifudiffusion.vae.pt" ) # ... 其他模型

# 下载SD模型
for model in "${sd_models[@]}"; do
  url=${sd_model_urls[$model]}
  aria2c --console-log-level=error --summary-interval=10 --header="Authorization: Bearer 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" -c -x 16 -k 1M -s 16 -d ${SD_MODEL_DIR} -o ${model} ${url}
done

# 下载VAE模型
for model in "${vae_models[@]}"; do
  url=${vae_model_urls[$model]}
  aria2c --console-log-level=error --summary-interval=10 --header="Authorization: Bearer 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" -c -x 16 -k 1M -s 16 -d ${VAE_MODEL_DIR} -o ${model} ${url}
done