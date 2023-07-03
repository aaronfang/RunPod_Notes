#!/bin/bash

ROOT_DIR="/workspace"    # 项目根目录
LORA_SCRIPTS_DIR="${ROOT_DIR}/lora-scripts"    # Akegarasu库克隆路径
SD_SCRIPTS_DIR="${LORA_SCRIPTS_DIR}/sd-scripts"    # sd_scripts路径
DEFAULT_SD_MODEL_DIR="${LORA_SCRIPTS_DIR}/sd-models"    # SD模型默认下载地址
ALT_SD_MODEL_DIR="${ROOT_DIR}/stable-diffusion-webui/models/stable-difusion" # 备选SD模型目录





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

echo "下载模型文件..."
# 检查目录中是否包含名为v1-5-pruned或者v1-5-pruned-emaonly的文件，后缀是.ckpt或.safetensors
contains_files() {
    for filename in "$1"/*; do
        base=$(basename -- "$filename")
        base_without_ext="${base%.*}"
        if [[ $base_without_ext == "v1-5-pruned" || $base_without_ext == "v1-5-pruned-emaonly" ]]; then
            if [[ $base == *.ckpt || $base == *.safetensors ]]; then
                return 0
            fi
        fi
    done
    return 1
}
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

# Run run_gui.sh script
# find /path/to/directory -name "*.sh" -exec chmod +x {} \;
chmod +x run_gui.sh
./run_gui.sh --host "0.0.0.0" --tensorboard-host "0.0.0.0"

# Deactivate the virtual environment
deactivate
