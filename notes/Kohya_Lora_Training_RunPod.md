# Lora Training with Kohya_ss in RunPod

> 1x RTX 3090 or RTX 4090 with 24GB VRAM  
> Runpod/stable-diffusion:web-automatic-8.0.3  
> Storage: 10GB Container Disk, 50GB+ Volume Disk  

1. Open https://www.runpod.io/
2. Community Cloud search for a 24GB VRAM GPU such as RTX 3090
3. Deploy a new pod and wait for it to be ready to connect
4. hit connect button and select "connect to Jupiter Lab". (Share the link by RMB on the link and copy link address)
5. navigate to /workspace/ folder
6. launch a terminal and run the following commands:
    ```bash
    chmod +x kohya_autodeploy.sh
    ./kohya_autodeploy.sh
    ```
7. after deplyment, kohya gui will be available at a shared link. click to open it.
8. now you can upload image dataset  
on local machine, run the following command:
```bash
runpodctl send -f /path/to/your/dataset
```
9. on RunPod, navigate to `/workspace/kohya_ss/image_input` folder, then run the following command:
```bash
runpodctl receive 8338-galileo-collect-fidel
```
10. sd model is located at `/workspace/sd-models/` folder. 

Reference:  
https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Install-Kohya-LoRA-Web-UI-On-RunPod.md