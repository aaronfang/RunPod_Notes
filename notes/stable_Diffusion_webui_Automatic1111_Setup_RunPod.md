# Stable Diffusion Webui Automatic1111 Setup
> 1x RTX 3090 or RTX 4090 with 24GB VRAM  
> Runpod/stable-diffusion:web-automatic-8.0.3  
> Storage: 10GB Container Disk, 50GB+ Volume Disk  
> 
### Install Latest Automatic1111 Web UI and DreamBooth Extension And Cuda and cuDNN DLL Libraries on RunPod  

1. Open https://www.runpod.io/
2. Deploy a new pod and wait for it to be ready to connect
3. hit connect button and select "`connect to Jupiter Lab`". (Share the link by RMB on the link and copy link address)
4. upload files to the root folder of the pod.  
    - `a_edit_relauncher.py`  -- this file will edit the relauncher.py file to make it only run webui once.  
    - `b_auto_deploy.py`  -- this file will install the necessary models and dreambooth extension automatically.  
    - `relaunch_webui.py`  -- this file will relaunch the webui.  
    - `webui-user.sh` -- this is the modified version of the original webui-user.sh file.  
    - `config.json` -- this is the modified version of the original config.json file.  
5. run the `a_edit_relauncher.py` file in the root folder of the pod. it will edit the `relauncher.py` file to make it only run once.
    ```bash
     python a_edit_relauncher.py
    ```
6. restart the pod. (to make the changes take effect)
7. run the `b_auto_deploy.py` file in the root folder of the pod. it will install the necessary models and dreambooth extension automatically.
    ```bash
    python b_auto_deploy.py
    ```
8. after that, webui will be launched already.  
you can go to connect tab and click "`Connect to HTTP Service [Port 3000]`" to see the webui. (if you see "Running on local URL: http://0.0.0.0:3000", it means that the webui has launched.)
9. if for any reason, you want to manually start web ui instance, or you turned off pod and started again later here below command:
    ```bash
    python relaunch_webui.py
    ```
10. when you are done with the webui, you need to send output images to your local computer. you can run the below command to do that. (you need to have `runpodctl` installed on your computer, read [RunpodCTL_guide.md](https://github.com/aaronfang/RunPod_Notes/blob/main/notes/RunpodCTL_guide.md) for more information)
    ```bash
    python send_output.py
    ```

Reference:  
- https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Install-DreamBooth-Extension-On-RunPod.md  
- https://github.com/trytofly94/RunpodSD-Customizer