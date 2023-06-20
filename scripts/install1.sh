#!/bin/bash

# modify relauncher.py to only run once
sed -i 's/while True:/while (n<1):/g' relauncher.py

# kill any existing webui
fuser -k 3000/tcp

# Update package lists
apt update

# update webui to latest version
cd /workspace/stable-diffusion-webui
git checkout master
git pull

# modify webui-user.sh
curl -o /workspace/stable-diffusion-webui/webui-user.sh https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/webui-user-pt1.sh

# remove old venv
rm -r venv

# install cuda and cudnn
yes | apt install -y libcudnn8=8.9.2.26-1+cuda11.8 libcudnn8-dev=8.9.2.26-1+cuda11.8 --allow-change-held-packages

# start webui
python relauncher.py