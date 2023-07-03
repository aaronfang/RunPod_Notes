# Run Akegarasu Lora Training in RunPod

> 1x RTX 3090 or RTX 4090 with 24GB VRAM  
> Runpod/stable-diffusion:web-automatic-8.0.3  
> Storage: 20GB Container Disk, 50GB+ Volume Disk  

1. Open https://www.runpod.io/
2. Community Cloud search for a 24GB VRAM GPU such as RTX 3090
3. Deploy a new pod and wait for it to be ready to connect
4. hit connect button and select "connect to Jupiter Lab".  
5. navigate to /workspace/ folder
6. upload an image to /workspace/ folder. (the image better be a headshot image with a simple background)  
7. launch a terminal and run the following commands:
    ```bash
    chmod +x autodeploy_akegarasu.sh
    ./autodeploy_akegarasu.sh
    ```

Reference:  
https://github.com/Akegarasu/lora-scripts