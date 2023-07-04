#!/bin/bash

ROOT_DIR="/workspace"    # 项目根目录
KOYHA_DIR="${ROOT_DIR}/kohya_ss"    # Kohya库克隆路径
DEFAULT_SD_MODEL_DIR="${KOYHA_DIR}/sd-models"    # SD模型默认下载地址
ALT_SD_MODEL_DIR="${ROOT_DIR}/stable-diffusion-webui/models/stable-difusion" # 备选SD模型目录

# Clone the repository
if [ ! -d "kohya_ss" ]; then
  git clone https://github.com/bmaltais/kohya_ss.git
fi

# Navigate into the cloned directory
cd kohya_ss || exit
# Run setup script
chmod +x ./setup-runpod.sh
./setup-runpod.sh

# 检查默认SD模型目录是否包含需要的文件
if contains_files $DEFAULT_SD_MODEL_DIR; then
    SD_MODEL_DIR=$DEFAULT_SD_MODEL_DIR
    echo "v1.5模型已存在于{$SD_MODEL_DIR}"
# 否则检查备选SD模型目录是否包含需要的文件
elif contains_files $ALT_SD_MODEL_DIR; then
    SD_MODEL_DIR=$ALT_SD_MODEL_DIR
    echo "v1.5模型已存在于{$SD_MODEL_DIR}"
else
    # 如果两个目录都不包含需要的文件，则下载文件到默认目录
    echo "v1.5模型不存在，正在下载到{$DEFAULT_SD_MODEL_DIR}..."
    SD_MODEL_DIR=$DEFAULT_SD_MODEL_DIR
    if [ ! -f "${SD_MODEL_DIR}/v1-5-pruned.ckpt" ]; then
      wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors -P "${SD_MODEL_DIR}"
    fi
fi

# 启动GUI
echo "启动GUI..."
./gui.sh --share --listen=0.0.0.0 --headless