import os
from accelerate.utils import write_basic_config
import subprocess

# 初始化常量
ROOT_DIR = "/workspace"
SD_SCRIPTS_DIR = os.path.join(ROOT_DIR, "sd-scripts")    # kohya库克隆路径
ACCELERATE_CONFIG_PATH = os.path.join(ROOT_DIR, "accelerate_config.yaml")   # accelerate库config文件写入地址

# 如果你想用自己的配置文件，或者采样文件，请填入下方 `填入意味着启用`
config_file_self_path = "" # 请替换为你自己的配置文件路径
sample_prompts_self_path = "" # 请替换为你自己的采样文件路径

os.chdir(ROOT_DIR)

if not os.path.exists(ACCELERATE_CONFIG_PATH):
    write_basic_config(save_location=ACCELERATE_CONFIG_PATH)

os.chdir(SD_SCRIPTS_DIR)

#开始训练！
command = [
    "accelerate",
    "launch",
    "--config_file=" + ACCELERATE_CONFIG_PATH,
    "--num_cpu_threads_per_process=8",
    "train_network.py",
    "--config_file=" + (config_file_self_path if config_file_self_path else "config_file.toml"),
    "--sample_prompts=" + (sample_prompts_self_path if sample_prompts_self_path else "sample_prompts.txt"),
]

process = subprocess.Popen(command)
process.wait()

os.chdir(ROOT_DIR)
