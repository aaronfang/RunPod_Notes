#!/bin/bash

ROOT_DIR="/workspace"    # 项目根目录
LORA_SCRIPTS_DIR="${ROOT_DIR}/lora-scripts"    # Akegarasu库克隆路径
SD_SCRIPTS_DIR="${LORA_SCRIPTS_DIR}/sd-scripts"    # sd_scripts路径
SD_MODEL_DIR="${LORA_SCRIPTS_DIR}/sd-models"    # SD模型下载地址

# 克隆Akegarasu库
if [ ! -d "lora-scripts" ]; then
  git clone --recurse-submodules https://github.com/Akegarasu/lora-scripts
fi

# 进入lora-scripts目录
cd "$LORA_SCRIPTS_DIR" || exit

# 检查当前环境中是否存在虚拟环境，如果没有则创建
if [ ! -d "venv" ]; then
  echo "正在创建虚拟环境..."
  python -m venv venv
  check "创建虚拟环境失败，请检查 python 是否安装完毕以及 python 版本是否为64位版本的python 3.10、或python的目录是否在环境变量PATH内。"
fi
# 如果虚拟环境存在，则激活虚拟环境
source venv/bin/activate

# 安装torch和xformers
pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
pip install --upgrade xformers==0.0.19

# 安装其他依赖
cd "$SD_SCRIPTS_DIR" || exit
pip install --upgrade -r requirements.txt
pip install --upgrade lion-pytorch lycoris-lora dadaptation fastapi uvicorn wandb

# 退回到lora-scripts目录
cd "$LORA_SCRIPTS_DIR" || exit

echo "脚本依赖安装完成"


echo "正在下载模型文件..."
if [ ! -f "${SD_MODEL_DIR}/v1-5-pruned.ckpt" ]; then
  wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt -P ${SD_MODEL_DIR}
fi

# Run run_gui.sh script
./run_gui.sh --host "0.0.0.0" --tensorboard-host "0.0.0.0"

# Deactivate the virtual environment
deactivate
