#!/bin/bash

fuser -k 3000/tcp

curl -o /workspace/stable-diffusion-webui/webui-user.sh https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/webui-user-pt2.sh

source /workspace/venv/bin/activate 

pip install xformers==0.0.20

yes | pip uninstall torch torchvision torchaudio

yes | pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install -r /workspace/stable-diffusion-webui/extensions/sd_dreambooth_extension/requirements.txt

cd /workspace/stable-diffusion-webui

python relauncher.py