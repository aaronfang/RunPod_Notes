# Lora Training with Kohya_ss in RunPod

> 1x RTX 3090  
> RunPod Stable Diffusion v1.5+v2  
> Storage: 10GB Container Disk, 50GB Volume Disk  

1. Open https://www.runpod.io/
2. Community Cloud search for a 24GB VRAM GPU such as RTX 3090
3. Deploy a new pod and wait for it to be ready to connect
4. hit connect button and select "connect to Jupiter Lab". (Share the link by RMB on the link and copy link address)
5. navigate to /workspace/ folder
6. launch a terminal and run the following commands:
    ```bash
    git clone https://github.com/bmaltais/kohya_ss.git

    cd kohya_ss

    python3 -m venv venv

    source venv/bin/activate

    ./setup.sh -n
    ```
7. after installation is finished, You will get this error during above file installation. Ignore it :  `ERROR: Failed building wheel for tensorrt ERROR: Could not build wheels for tensorrt, which is required to install pyproject.toml-based projects.`  
Also you might encounter an error about `missing tkinter`. If so, run the following command:
    ```bash
    source venv/bin/activate

    apt update

    apt-get install python3.10-tk

    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

    yes | apt install -y libcudnn8=8.7.0.84-1+cuda11.8 libcudnn8-dev=8.7.0.84-1+cuda11.8 --allow-change-held-packages
    ```
### After installation
1. Restart the pod
2. navigate to `/workspace/kohya_ss` folder
3. launch a terminal and run the following commands:
    ```bash
    bash gui.sh --share
    ```
**Now supports xformers and AdamW8bit as well**

### Prepare for training
1. download stable diffusion 1.5 model from huggingface:
```bash
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt
```
2. upload image dataset  
on local machine, run the following command:
```bash
runpodctl send -f /path/to/your/dataset
```
3. on RunPod, navigate to `/workspace/kohya_ss/image_input` folder, then run the following command:
```bash
runpodctl receive 8338-galileo-collect-fidel
```

Reference:  
https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Install-Kohya-LoRA-Web-UI-On-RunPod.md