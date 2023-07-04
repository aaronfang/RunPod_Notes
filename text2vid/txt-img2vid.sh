#!/bin/bash

set -e  # if a command fails it stops the execution
set -u  # script fails if trying to access to a declared variable

WORK_DIR="/workspace"    # 项目根目录
REPO_TEXT_TO_VIDEO="https://github.com/camenduru/Text-To-Video-Finetuning"
REPO_POTAT1ALM="https://github.com/ailostmedia/Potat1ALM"

cd "$WORK_DIR" || exit

# 检查当前环境中是否存在虚拟环境，如果没有则创建
if [ ! -d "venv" ]; then
  echo "正在创建虚拟环境..."
  python -m venv venv
fi

# 如果虚拟环境存在，则激活虚拟环境
source venv/bin/activate

# 安装Python依赖包
pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 torchtext==0.14.1 torchdata==0.5.1 --extra-index-url https://download.pytorch.org/whl/cu116 -U
pip install git+https://github.com/huggingface/diffusers transformers accelerate imageio[ffmpeg] -U einops omegaconf decord xformers==0.0.16 safetensors
pip install triton einops gradio

# Clone repositories
git clone -b dev "$REPO_TEXT_TO_VIDEO"
git clone "$REPO_POTAT1ALM"

cd $REPO_TEXT_TO_VIDEO || exit
pip install -r requirements.txt

cd "$WORK_DIR" || exit
# Move the inference.py file
mv "$WORK_DIR"/Potat1ALM/inference.py "$WORK_DIR"/Text-To-Video-Finetuning/


#############################################################
# Step 2 (Mandatory) - Install Potat1 or ZeroScope (or both)
#############################################################

# Install Potat1
#default 1024 x 576 - try 800 x 448 for colab
cd "$WORK_DIR"/
git clone https://huggingface.co/camenduru/potat1

#@title STEP2: Install ZeroScope 576
#default 576 x 320
cd "$WORK_DIR"/
git clone https://huggingface.co/cerspense/zeroscope_v2_576w

#@title STEP2: Install ZeroScope XL
#default 1024 x 576 - try 800 x 448 for colab
cd "$WORK_DIR"/
git clone https://huggingface.co/cerspense/zeroscope_v2_XL

#@title STEP2: Install ZeroScope 448
#default 448 x 256
cd "$WORK_DIR"/
git clone https://huggingface.co/cerspense/zeroscope_v2_dark_30x448x256


###========== Step 3 - Text to Video ==========
cd "$WORK_DIR"/Text-To-Video-Finetuning
import torch
import random
import numpy as np

# could be a json file
#@markdown #### Be sure you have installed the model you want in step 2
model = "potat1" #@param ["potat1", "zeroscope_v2_dark_30x448x256", "zeroscope_v2_576w", "zeroscope_v2_XL"]
prompt = "extremely detailed, Futuristic Cityscape, blade runner, extremely cloudy, awardwinning, best quality, 8k" #@param {type:"string"}
negative = "text, watermark, copyright, blurry, nsfw, noise, quick motion, bad quality, flicker, dirty, ugly, fast motion, quick cuts, fast editing, cuts" #@param {type:"string"}
prompt = f"\"{prompt}\""
negative = f"\"{negative}\""
num_steps = 25 #@param {type:"raw"}
guidance_scale = 23 #@param {type:"raw"}
width = 800 #@param {type:"raw"}
height = 448 #@param {type:"raw"}
fps = 10 #@param {type:"raw"}
num_frames = 30 #@param {type:"raw"}
seedManual = "Random"
seeding = "Random" #@param ["Random", "Manual"]
inputSeed = 7106521602475165645 #@param {type:"raw"}
if seeding == "Random":
  thisSeed = random.randint(0, ((1<<63)-1))
  print("seed is " + str(thisSeed))
else:
  thisSeed = inputSeed

thisHeight = int(round(height/8.0)*8.0)
thisWidth = int(round(width/8.0)*8.0)

thisModel=""$WORK_DIR"/"+model
!python inference.py -m {thisModel} -p {prompt} -n {negative} -W {thisWidth} -H {thisHeight} -o "$WORK_DIR"/outputs -d cuda -x -s {num_steps} -g {guidance_scale} -f {fps} -T {num_frames} -seed {thisSeed}
#-seed {thisSeed}

###========== Optional: Image to Vid ==========
#@title Img2Vid Step 1: Install 3D Photo inpainting
apt -y install -qq aria2 xvfb
pip install vispy transforms3d networkx
cd "$WORK_DIR"/
git clone -b dev https://github.com/camenduru/3d-photo-inpainting
cd "$WORK_DIR"/3d-photo-inpainting
git clone https://github.com/camenduru/BoostingMonocularDepth

aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/3d-photo-inpainting/resolve/main/color-model.pth -d "$WORK_DIR"/3d-photo-inpainting/checkpoints -o color-model.pth
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/3d-photo-inpainting/resolve/main/depth-model.pth -d "$WORK_DIR"/3d-photo-inpainting/checkpoints -o depth-model.pth
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/3d-photo-inpainting/resolve/main/edge-model.pth -d "$WORK_DIR"/3d-photo-inpainting/checkpoints -o edge-model.pth
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/3d-photo-inpainting/resolve/main/model.pt -d "$WORK_DIR"/3d-photo-inpainting/checkpoints -o model.pt

aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/3d-photo-inpainting/resolve/main/latest_net_G.pth -d "$WORK_DIR"/3d-photo-inpainting/BoostingMonocularDepth/pix2pix/checkpoints/mergemodel -o latest_net_G.pth
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/3d-photo-inpainting/resolve/main/model-f46da743.pt -d "$WORK_DIR"/3d-photo-inpainting/BoostingMonocularDepth/midas -o model.pt

#@title Img2Vid Step 2: Select Photo - Subject should be in center (use Jpg)
import os
import shutil
from google.colab import drive
from google.colab import files
def reformat_photo(photo):
    """function to reformat photo"""


#@markdown ### Select an uploading method
upload_method = "Upload" #@param ["Upload", "Custom Path"]

# remove previous input video
if os.path.isfile('"$WORK_DIR"/3d-photo-inpainting/image/test.jpg'):
    os.remove('"$WORK_DIR"/3d-photo-inpainting/image/test.jpg')

if upload_method == "Upload":
    uploaded = files.upload()
    for filename in uploaded.keys():
        os.rename(filename, '"$WORK_DIR"/3d-photo-inpainting/image/test.jpg')
    PATH_TO_YOUR_PHOTO = '"$WORK_DIR"/3d-photo-inpainting/image/test.jpg'

elif upload_method == 'Custom Path':
    if not 'drive' in globals():
        drive.mount('"$WORK_DIR"/drive')
    #@markdown ``Add the full path to your video on your Gdrive `` 👇
    PATH_TO_YOUR_PHOTO = '"$WORK_DIR"/3d-photo-inpainting/image/test.jpg' #@param {type:"string"}
    if not os.path.isfile(PATH_TO_YOUR_PHOTO):
        print("ERROR: File not found!")
        raise SystemExit(0)

if upload_method == "Upload":
  print("Input photo")

else:
    if os.path.isfile(PATH_TO_YOUR_PHOTO):
        shutil.copyfile(PATH_TO_YOUR_PHOTO, ""$WORK_DIR"/3d-photo-inpainting/image/test.jpg")
        print("Input Photo")
        showVideo(PATH_TO_YOUR_PHOTO)


#@title Img2Vid Step 3: Run 3D Photo inpainting
pip install pyyaml
#@markdown ### Select the video type
video_type = "zoom-in" #@param ["zoom-in", "dolly-zoom-in", "circle", "swing"]
#@markdown ### Select the trajectory type (straight line to end video after move, circle to end at start)
trajectory_type = "double-straight-line" #@param ["double-straight-line", "circle"]
#@markdown ### Input the trajectories (use between 0 and .05)
#@markdown ### X (Negative is right, Positive is left)
x = 0.00 #@param {type:"raw"}
#@markdown ### Y (Negative is down, Positive is up)
y = 0.015 #@param {type:"raw"}
#@markdown ### Z (Negative is toward subject, Positive is away)
z = -0.05 #@param {type:"raw"}
#@markdown ### input the fps and frames for video
fps = 24 #@param {type:"raw"}
num_frames = 72 #@param {type:"raw"}

import yaml
cd "$WORK_DIR"/3d-photo-inpainting

with open('argument.yml', 'r') as file:
  arguments = file.readlines()

#yaml_data[5] = "fps: "+ str(fps)
arguments[5] = "fps: "+ str(fps) +"\n"
arguments[6] = "num_frames: "+ str(num_frames) +"\n"
arguments[7] = "x_shift_range: [" +str(x) +"]\n"
arguments[8] = "y_shift_range: [" +str(y) +"]\n"
arguments[9] = "z_shift_range: [" +str(z) +"]\n"
arguments[10] = "traj_types: [" +str(trajectory_type) +"]\n"
arguments[11] = "video_postfix: [" +str(video_type) +"]\n"

with open('argument.yml', 'w') as file:
  file.writelines(arguments)

xvfb-run -s "-screen 0 1280x720x24" python main.py --config argument.yml


#@title Img2Vid STEP 4: V2V with ZeroScope (Will Need Interpolating)
cd "$WORK_DIR"/Text-To-Video-Finetuning
import torch
import random
import numpy as np

#@markdown ### Select the model (be sure to have installed in Step 2)
model = "zeroscope_v2_dark_30x448x256" #@param ["potat1", "zeroscope_v2_dark_30x448x256", "zeroscope_v2_576w", "zeroscope_v2_XL"]
#@markdown ### Copy Video Path from 3d-photo-inpainting/video
video_path = "" #@param {type:"string"}
video_weight = .2 #@param {type:"raw"}
#@markdown ### Fill in prompt and parameters!
prompt = "Extremely Detailed, dynamic shot, action, 80s live action medieval fantasy film shot of a young hero riding a hovercycle high in the clouds, stormy, hyperrealistic, best quality, awardwinning" #@param {type:"string"}
negative = "blurry, text, watermark, copyright, blurry, nsfw, noise, quick motion, bad quality, flicker, dirty, ugly, fast motion, quick cuts, fast editing, cuts" #@param {type:"string"}
prompt = f"\"{prompt}\""
negative = f"\"{negative}\""
num_steps = 50 #@param {type:"raw"}
guidance_scale = 23 #@param {type:"raw"}
width = 448 #@param {type:"raw"}
height = 256 #@param {type:"raw"}
fps = 10 #@param {type:"raw"}
num_frames = 30 #@param {type:"raw"}
#@markdown ### Seeding not currently working for v2v (WIP)
seedManual = "Random"
seeding = "Random" #@param ["Random", "Manual"]

inputSeed = 6708511088475640657 #@param {type:"raw"}
if seeding == "Random":
  thisSeed = random.randint(0, ((1<<63)-1))
  print("seed is " + str(thisSeed))
else:
  thisSeed = inputSeed

thisHeight = int(round(height/8.0)*8.0)
thisWidth = int(round(width/8.0)*8.0)
thisModel=""$WORK_DIR"/"+model
thisVideoPath = str(video_path)
python inference.py -m {thisModel} -p {prompt} -n {negative} -W {thisWidth} -H {thisHeight} -o "$WORK_DIR"/outputs -d cuda -x -s {num_steps} -g {guidance_scale} -f {fps} -T {num_frames} -seed {thisSeed} -i {thisVideoPath} -iw {video_weight}
#-seed {thisSeed}


###========== Optional - V2V (Upload your own or use ZeroScope below) ==========
#@title V2V Step 1: Run ZeroScope (Optional)
%cd "$WORK_DIR"/Text-To-Video-Finetuning
import torch
import random
import numpy as np
"""
torch.use_deterministic_algorithms(True)

torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic=True
random.seed(2)
np.random.seed(2)
torch.manual_seed(2)
torch.cuda.manual_seed(2)
torch.cuda.manual_seed_all(2)
torch.manual_seed(0)
"""
#print("seed is " + str(torch.seed()))

#seeding = "Random"
#thisSeed = 123;


#preset = "Manual"
# while True:

prompt = "extremely detailed, Futuristic Cityscape, blade runner, extremely cloudy, awardwinning, best quality, 8k" #@param {type:"string"}
negative = "text, watermark, copyright, blurry, nsfw, noise, quick motion, bad quality, flicker, dirty, ugly, fast motion, quick cuts, fast editing, cuts, blurry" #@param {type:"string"}
prompt = f"\"{prompt}\""
negative = f"\"{negative}\""
num_steps = 25 #@param {type:"raw"}
guidance_scale = 23 #@param {type:"raw"}
fps = 10 #@param {type:"raw"}
num_frames = 30 #@param {type:"raw"}
seedManual = "Random"
seeding = "Random" #@param ["Random", "Manual"]

inputSeed = 5939699337684636079 #@param {type:"raw"}
if seeding == "Random":
  thisSeed = random.randint(0, ((1<<63)-1))
  print("seed is " + str(thisSeed))
else:
  thisSeed = inputSeed

!python inference.py -m "$WORK_DIR"/zeroscope_v2_dark_30x448x256 -p {prompt} -n {negative} -W 448 -H 256 -o "$WORK_DIR"/outputs -d cuda -x -s {num_steps} -g {guidance_scale} -f {fps} -T {num_frames} -seed {thisSeed}
#-seed {thisSeed}