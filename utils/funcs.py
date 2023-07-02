from subprocess import run
import os
import requests
from urllib.parse import urlparse
from tqdm import tqdm

#######################################
# FUNCTIONS
#######################################

# function to run bash command
def run_cmd(cmd, cwd=None):
    run(cmd, cwd=cwd, shell=True, check=True)

def run_cmd_return(cmd):
    result = run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

# kill port if occupied
def kill_port_if_occupied(port):
    cmd = f"fuser -k {port}/tcp"
    try:
        return_code, stdout, stderr = run_cmd_return(cmd)
        if stdout:
            print(f"Port {port} is occupied. Killing the process...")
            return_code, stdout, stderr = run_cmd_return(cmd)
            if return_code == 0:
                print(f"Process on port {port} killed successfully.")
            else:
                print(f"Failed to kill the process on port {port}.")
        else:
            print(f"Port {port} is not occupied.")
    except Exception as e:
        print(f"An error occurred while executing the command: {e}")

# replace text in file
def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(old_text, new_text)
    with open(file_path, 'w') as file:
        file.write(content)

# update git repo function
def update_git_repo(repo_path, repo_url=None, force_reset=False, update_submodules=False, branch=None):
    # clone repository if repo_url is provided and repo doesn't exist
    if repo_url and not os.path.exists(repo_path):
        parent_dir = os.path.dirname(repo_path)
        if update_submodules:
            run(['git', 'clone', '--recurse-submodules', repo_url, repo_path], check=True)
        else:
            run(['git', 'clone', repo_url, repo_path], check=True)
        print(f"Git repository cloned from {repo_url} to {repo_path} successfully!")
    elif os.path.exists(repo_path):
        # change working directory
        os.chdir(repo_path)

        # checkout specific branch if provided
        if branch:
            run(["git", "checkout", branch], check=True)
            print(f"Checked out branch {branch} in {repo_path} successfully!")

        # reset git repository if needed
        if force_reset:
            run(["git", "reset", "--hard"], check=True)
            print(f"Git repository in {repo_path} reset successfully!")
        
        # Check for submodules and update if present
        if update_submodules and os.path.isfile('.gitmodules'):
            run(["git", "pull"], check=True)
            run(["git", "submodule", "update", "--init", "--recursive"], check=True)
            print(f"Submodules in {repo_path} updated successfully!")
        else:
            # pull latest version if repo exists
            run(["git", "pull"], check=True)
            print(f"Git repository in {repo_path} pulled successfully!")

# download function from google drive
def gdown_func(id, output):
    run_cmd(f"gdown {id}", cwd=output)

# download function from url
def download_files(urls, output_path):
    for url in urls:
        parsed_url = urlparse(url)
        command = ""

        if 'civitai' in parsed_url.netloc:
            command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {url} -d {output_path}"
        elif 'huggingface' in parsed_url.netloc:
            filename = url.split('/')[-1]  # 获取url中的文件名
            command = f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M -o {filename} {url} -d {output_path}"
        elif 'google_drive_id' in url:
            gdown_func(url.split(':')[-1], output_path)
            continue

        result = os.system(command)
        if result == 0:
            print(f"{url} downloaded successfully!")
        else:
            print(f"An error occurred while downloading {url}.")

# download file from github
def download_file_from_github(repo_owner, repo_name, file_path, save_dir):
    base_url = "https://raw.githubusercontent.com"
    file_url = os.path.join(base_url, repo_owner, repo_name, 'main', file_path)
    
    response = requests.get(file_url)
    
    # make sure that the request was successful
    if response.status_code == 200:
        # make sure the save_dir exists
        os.makedirs(save_dir, exist_ok=True)
        
        with open(os.path.join(save_dir, os.path.basename(file_path)), 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")

def download_with_progress(url, dest_path):
        filename = os.path.basename(urlparse(url).path)
        response = requests.get(url, stream=True)
        total_length = int(response.headers.get('content-length', 0))

        with open(dest_path, "wb") as file, tqdm(
            desc=f"Downloading {filename}", total=total_length, unit="B", unit_scale=True
        ) as progress_bar:
            for data in response.iter_content(chunk_size=4096):
                file.write(data)
                progress_bar.update(len(data))
