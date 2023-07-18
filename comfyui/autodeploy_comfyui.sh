#! /bin/bash

ROOT_DIR=/workspace
COMFYUI_DIR=$ROOT_DIR/ComfyUI
MODEL_DIR=$COMFYUI_DIR/models
VAE_DIR=$MODEL_DIR/vae

# This script is used to deploy the ComfyUI to the server.
echo "克隆 ComfyUI 库..."
git clone https://github.com/comfyanonymous/ComfyUI
# change directory to ComfyUI
cd ComfyUI || exit

# 检查当前环境中是否存在虚拟环境，如果没有则创建
if [ ! -d "venv" ]; then
  echo "正在创建虚拟环境..."
  python -m venv venv
  check "创建虚拟环境失败，请检查 python 是否安装完毕以及 python 版本是否为64位版本的python 3.10、或python的目录是否在环境变量PATH内。"
fi
# 如果虚拟环境存在，则激活虚拟环境
source venv/bin/activate

echo "安装依赖"
# pip install xformers!=0.0.18 -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118 --extra-index-url https://download.pytorch.org/whl/cu117
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -U --pre xformers
pip install -r requirements.txt

# download the models from the google drive
echo "从google drive下载模型"
pip install gdown
# check if sd_xl_base_0.9.safetensors and sd_xl_refiner_0.9.safetensors are in $MODEL_DIR, download if not exists
if [ ! -f "$MODEL_DIR/sd_xl_base_0.9.safetensors" ]; then
    echo "没有找到sd_xl_base_0.9.safetensors，开始下载..."
    gdown '10MXEIKyyB57yugRbnkaX-Vcsdwthz4PK' -O $MODEL_DIR/sd_xl_base_0.9.safetensors
else
    echo "sd_xl_base_0.9.safetensors 已经存在。"
fi

if [ ! -f "$MODEL_DIR/sd_xl_refiner_0.9.safetensors" ]; then
    echo "没有找到sd_xl_refiner_0.9.safetensors，开始下载..."
    gdown '1MVwMJ3sLKvSAXtxExwrmdUIplN0r2GNq' -O $MODEL_DIR/sd_xl_refiner_0.9.safetensors
else
    echo "sd_xl_refiner_0.9.safetensors 已经存在。"
fi

# check if vae-ft-mse-840000-ema-pruned.safetensors is in $VAE_DIR, download if not exists
if [ ! -f "$VAE_DIR/vae-ft-mse-840000-ema-pruned.safetensors" ]; then
    echo "没有找到vae-ft-mse-840000-ema-pruned.safetensors，开始下载..."
    wget -c https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors -P $VAE_DIR
else
    echo "vae-ft-mse-840000-ema-pruned.safetensors 已经存在。"
fi

# echo "从 pastebin 下载SDXL的节点图"
# if [ ! -f "$COMFYUI_DIR/Workflow_ComfyUI_SDXL_0.9.json" ]; then
#     echo "没有找到Workflow_ComfyUI_SDXL_0.9.json，开始下载..."
#     wget https://pastebin.com/dl/sjhP8Pcj -O $COMFYUI_DIR/Workflow_ComfyUI_SDXL_0.9.json
#     wget https://pastebin.com/dl/brKr6QJc -O $COMFYUI_DIR/Workflow_ComfyUI_SDXL_0.9_v2.json
# else
#     echo "Workflow_ComfyUI_SDXL_0.9.json 已经存在。"
# fi

# --listen：字符串类型，指定服务器要监听的IP地址，默认为"127.0.0.1"。如果--listen参数提供了但没有值，将默认为"0.0.0.0"。
# --port：整数类型，设置服务器要监听的端口，默认为8188。
# --enable-cors-header：字符串类型，开启CORS (跨来源资源共享)，可以提供一个源（origin），或默认允许所有源（"*"）。
# --extra-model-paths-config：字符串类型，可以加载一个或多个extra_model_paths.yaml文件。
# --output-directory：字符串类型，设置ComfyUI的输出目录。
# --auto-launch：布尔值，如果设置，会在默认的浏览器中自动打开ComfyUI。
# --cuda-device：整数类型，设置这个实例要使用的CUDA设备的id。
# --dont-upcast-attention：布尔值，如果设置，将禁用注意力的上采样。这可能会提高速度，但也可能增加生成黑色图像的可能性。
# --force-fp32：布尔值，强制使用fp32精度。
# --force-fp16：布尔值，强制使用fp16精度。
# --fp16-vae：布尔值，以fp16运行VAE，可能会导致黑色图像。
# --bf16-vae：布尔值，以bf16运行VAE，可能会降低质量。
# --directml：整数类型，使用torch-directml。
# --preview-method：枚举类型，设置采样器节点的默认预览方法。
# --use-split-cross-attention：布尔值，使用分裂交叉注意力优化。
# --use-quad-cross-attention：布尔值，使用四次交叉注意力优化。
# --use-pytorch-cross-attention：布尔值，使用新的pytorch 2.0交叉注意力函数。
# --disable-xformers：布尔值，禁用xformers。
# --gpu-only：布尔值，将所有内容（文本编码器/CLIP模型等）存储并在GPU上运行。
# --highvram：布尔值，模型将保持在GPU内存中，不会在使用后卸载到CPU内存。
# --normalvram：布尔值，如果lowvram自动启用，使用此选项可以强制正常使用显存。
# --lowvram：布尔值，将unet分解成部分以减少显存使用。
# --novram：布尔值，当lowvram不够用时使用。
# --cpu：布尔值，使用CPU进行所有操作。
# --dont-print-server：布尔值，不打印服务器输出。
# --quick-test-for-ci：布尔值，用于连续集成的快速测试。
# --windows-standalone-build：布尔值，用于Windows独立构建，启用可能对大多数使用Windows独立构建的人有益的便利功能（如启动时自动打开页面）

echo "启动 ComfyUI"
python main.py --listen --port 8188 