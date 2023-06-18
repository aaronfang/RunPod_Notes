### install runpodCTL on your pod
in RunPod terminal, type the following command to install runpodctl
```bash
wget --quiet --show-progress https://github.com/Run-Pod/runpodctl/releases/download/v1.9.0/runpodctl-linux-amd -O runpodctl && chmod +x runpodctl && sudo cp runpodctl /usr/bin/runpodctl
```

### download online data with runpodCTL
if you want to download model from huggingface or civitai to your pod, you can do the following:
    a. navigate to the folder you want to download the model to, such as /workspace/stable-diffusion-webui/models/Stable-diffusion/
    b. launch a new terminal, type the following command:
    ```bash
    wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt
    ```

### install runpodCTL on your Macosx(ARM)
```bash
wget --quiet --show-progress https://github.com/runpod/runpodctl/releases/download/v1.9.0/runpodctl-darwin-arm -O runpodctl && chmod +x runpodctl && sudo mv runpodctl /usr/local/bin/runpodctl
```

### install runpodCTL on your Windows
1. navigate to the folder you want to download the model to, such as C:\
```powershell
wget https://github.com/runpod/runpodctl/releases/download/v1.9.0/runpodctl-win-amd -O runpodctl.exe
```
2. then add the folder to your PATH environment variable

### send files using runpodCTL
```bash
runpodctl send data.txt
```
Output should look like this:
```bash
Sending 'data.txt' (5 B)
Code is: 8338-galileo-collect-fidel
On the other computer run

runpodctl receive 8338-galileo-collect-fidel
```
Run the command on the other computer to receive the file:
```bash
runpodctl receive 8338-galileo-collect-fidel
```

References:  
https://github.com/runpod/runpodctl
