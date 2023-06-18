# Stable Diffusion Webui Automatic1111 Setup
> 1x RTX 4090  
> RunPod Stable Diffusion v1.5+v2  
> Storage: 10GB Container Disk, 50GB Volume Disk  
> 
### Install Latest Automatic1111 Web UI and DreamBooth Extension And Cuda and cuDNN DLL Libraries on RunPod  

1. Open https://www.runpod.io/
2. Community Cloud search for a 24GB VRAM GPU such as RTX 3090
3. Deploy a new pod and wait for it to be ready to connect
4. hit connect button and select "connect to Jupiter Lab". (Share the link by RMB on the link and copy link address)
5. change the "relauncher.py" inside the "stable-diffusion-webui" folder to the following:  
    replace:
    ```python
    while True:
    ```
    with:
    ```python
    while (n<1):
    ```
6. save the file and restart the pod. (sometime you need to reconnect the pod again)
7. go to /workspace/, upload install1.sh and install2.sh, by drag and drop them to the folder
8. open a terminal and run the following commands:
    ```bash
    chmod +x install1.sh
    ./install1.sh
    ```
9. wait for the installation to finish. When you see "Running on local URL: http://0.0.0.0:3000", it means that the first part of installation has been completed.
10. open a new terminal and run the following commands:
    ```bash
    chmod +x install2.sh
    ./install2.sh
    ```
11. wait for the installation to finish. When you see "Running on local URL: http://0.0.0.0:3000", it means that the second part of installation has been completed.
12. go to My Pods, click the pod you just created, and click "Connect" button. Then select "Connect to HTTP Service [Port 3000]". 
13. You should see the webui of stable diffusion.
14. go to settings tab, you can change the parameters as you want. (remember to click "Apply settings" button after you change the parameters, and Reload UI button after you apply the settings)
15. If you want to manually start web ui instance, or you turned off pod and started again later here below command:
    ```bash
    fuser -k 3000/tcp
    cd /workspace/stable-diffusion-webui
    python relauncher.py
    ```

### Important  
After restart your pod (turn off and turn on) start your web ui with below command. Otherwise you will get half speed. 
```bash
fuser -k 3000/tcp
yes | apt install -y libcudnn8=8.9.2.26-1+cuda11.8 libcudnn8-dev=8.9.2.26-1+cuda11.8 --allow-change-held-packages
cd /workspace/stable-diffusion-webui
python relauncher.py
```

Reference:
https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Install-DreamBooth-Extension-On-RunPod.md