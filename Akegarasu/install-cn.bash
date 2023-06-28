#!/usr/bin/bash

# 环境变量
export HF_HOME="huggingface"
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_CACHE_DIR=1

function check {
    if [ $? -ne 0 ]; then
        echo "$1"
        exit 1
    fi
}

if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python -m venv venv
    check "创建虚拟环境失败，请检查 python 是否安装完毕以及 python 版本是否为64位版本的python 3.10、或python的目录是否在环境变量PATH内。"
fi

source venv/bin/activate
check "激活虚拟环境失败。"

cd sd-scripts
echo "安装程序所需依赖..."
read -p "是否需要安装 Torch+xformers? [y/n] (默认为 y)" install_torch
if [ "$install_torch" == "y" ] || [ "$install_torch" == "Y" ] || [ -z "$install_torch" ]; then
    pip install torch==2.0.0+cu118 torchvision==0.15.1+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
    check "torch 安装失败，请删除 venv 文件夹后重新运行。"
    pip install -U -I --no-deps xformers==0.0.19
    check "xformers 安装失败。"
fi

pip install --upgrade -r requirements.txt
check "其他依赖安装失败。"
pip install --upgrade lion-pytorch dadaptation
check "Lion、dadaptation 优化器安装失败。"
pip install --upgrade lycoris-lora
check "lycoris 安装失败。"
pip install --upgrade fastapi uvicorn
check "UI 所需依赖安装失败。"
pip install --upgrade wandb
check "wandb 安装失败。"

echo "安装 bitsandbytes..."
cp bitsandbytes_windows/*.dll ../venv/lib/python3.*/site-packages/bitsandbytes/
cp bitsandbytes_windows/cextension.py ../venv/lib/python3.*/site-packages/bitsandbytes/cextension.py
cp bitsandbytes_windows/main.py ../venv/lib/python3.*/site-packages/bitsandbytes/cuda_setup/main.py

echo "安装完毕"
