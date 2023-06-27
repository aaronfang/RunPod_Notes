# Stable Diffusion Webui Automatic1111 Setup
> 1x RTX 3090 or RTX 4090 with 24GB VRAM  
> Runpod/stable-diffusion:web-automatic-8.0.3  
> Storage: 10GB Container Disk, 50GB+ Volume Disk  
> 
### Install Latest Automatic1111 Web UI and DreamBooth Extension And Cuda and cuDNN DLL Libraries on RunPod  

1. Open https://www.runpod.io/
2. Deploy a new pod. Before start, you need to specify the port to be like `8888`, `7860`. if you rented more then one GPU, you should add extra ports `7861`, `7862`... you can also add an environment valable to prevent the webui from running automatically infinitely.  
    - `RUNPOD_STOP_AUTO` = `1`
3. hit connect button and select "`connect to Jupiter Lab`". (Share the link by RMB on the link and copy link address)
4. upload files to the root folder of the pod.  
    - `autodeploy_webui.py`  -- this file will install the necessary models and dreambooth extension automatically.  
    - `launch_webui.py` -- this file will launch the webui.
    - `config.json` -- this is the modified version of the original config.json file. 
    - `send_output.py` -- this file will send the output images to your local computer.  
    - `webui-user.sh` -- this is the modified version of the original webui-user.sh file.  
5. run the `autodeploy_webui.py` file in the root folder of the pod. it will install the necessary models and dreambooth extension automatically. You may need to modify the `autodeploy_webui.py` file to change the contents you want to install.
    ```bash
    python autodeploy_webui.py
    ```
6. wait untill you see "========== All Done! ==========" in the terminal. then you can run `launch_webui.py` to launch the webui. you can run this file multiple times if your server have more than one GPU.
    ```bash
    python launch_webui.py
    ```
you can go to connect tab and click "`Connect to HTTP Service [Port 7860]`" to open the webui page. 
7. when you are done with the webui, if you want to send output images to your local computer. you can run the below command to do that. (you need to have `runpodctl` installed on your computer, read [RunpodCTL_guide.md](https://github.com/aaronfang/RunPod_Notes/blob/main/notes/RunpodCTL_guide.md) for more information)
    ```bash
    python send_output.py
    ```

Reference:  
- https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Install-DreamBooth-Extension-On-RunPod.md  
- https://github.com/trytofly94/RunpodSD-Customizer