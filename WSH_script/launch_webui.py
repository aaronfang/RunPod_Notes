import os
import sys
import toml

# 初始化常量
ROOT_DIR = "/workspace"
SD_SCRIPTS_DIR = os.path.join(ROOT_DIR, "sd-scripts")    # kohya库克隆路径
WEBUI_DIR = os.path.join(ROOT_DIR, "kohya-config-webui")   # webui库克隆路径
SD_MODEL_DIR = os.path.join(ROOT_DIR, "Lora/sd_model")    # SD模型下载地址
VAE_MODEL_DIR = os.path.join(ROOT_DIR, "Lora/vae_model")    # VAE模型下载地址
# 在此根据你的实际路径进行配置
DEFAULT_INPUT_DIR = "<Your Input Path>"    # 训练集地址
DEFAULT_REG_DIR = "<Your Reg Path>"    # 正则化地址
DEFAULT_OUPUT_DIR = "<Your Output Path>"    # 模型输出地址
DEFAULT_WEBUI_SAVE_DIR = "<Your Webui Save Path>"    # 保存webui参数文件地址
ACCELERATE_CONFIG_PATH = os.path.join(ROOT_DIR, "accelerate_config.yaml")   # accelerate库config文件写入地址

sys.path.append(os.path.join(WEBUI_DIR, "module"))
from kohya_config_webui import create_demo


def creat_save_toml(save_dir):
    #生成适用于Linux环境的webui参数保存文件colab.toml
    #写入路径
    other={"write_files_dir":SD_SCRIPTS_DIR}
    #材料、模型、输出路径
    param={
        "train_data_dir":DEFAULT_INPUT_DIR,
        "reg_data_dir":DEFAULT_REG_DIR,
        "base_model_dir":SD_MODEL_DIR,
        "vae_model_dir":VAE_MODEL_DIR,
        "output_dir":DEFAULT_OUPUT_DIR,
        "lowram":True,
    }

    save_dict = {"other":other, "param":param}
    #写入文件
    save_name = "colab.toml"
    save_path = os.path.join( save_dir, save_name )
    os.makedirs(save_dir, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write( toml.dumps(save_dict) )

creat_save_toml(DEFAULT_WEBUI_SAVE_DIR)

#导入并生成demo
launch_param = [f"--save_dir={DEFAULT_WEBUI_SAVE_DIR}",
        f"--save_name=kohya_config_webui_save.toml",
        f"--read_dir={DEFAULT_WEBUI_SAVE_DIR}"
]

os.chdir( os.path.join(WEBUI_DIR, "module") )
demo = create_demo(launch_param)

# 启动
demo.launch(share=True)
