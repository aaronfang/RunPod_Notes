#! /bin/bash

# This script is used to automatically deploy the LineShadowGen application
# clone the repository
git clone https://github.com/tori29umai0123/LineShadowGen.git
cd /workspace/LineShadowGen || exit
# install virtual environment
apt-get update
apt-get install -y python3-venv
# create a virtual environment
python -m venv venv
source venv/bin/activate
# install the required packages
pip install -r requirements.txt
# install pytorch
pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
# download models
python /workspace/LineShadowGen/Scripts/models_dl.py
# run the application
python /workspace/LineShadowGen/colab_app.py share
# deactivate the virtual environment
deactivate