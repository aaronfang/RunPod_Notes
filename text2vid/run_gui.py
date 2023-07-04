import gradio as gr
import json
import os

# 加载参数
with open('params.json', 'r') as f:
    params = json.load(f)

# 函数定义，将会在点击按钮后运行
def run_inference(model, prompt, negative, num_steps, guidance_scale, width, height, fps, num_frames, seed):
    thisModel=os.path.join("D:/sd_webui/txt_img2vid" + model) # "D:\sd_webui\txt_img2vid"+model
    # 执行你的脚本，注意在这里我只是打印参数作为示例，你需要修改为实际的运行命令
    print(f'python inference.py -m {thisModel} -p {prompt} -n {negative} -W {width} -H {height} -o outputs -d cuda -x -s {num_steps} -g {guidance_scale} -f {fps} -T {num_frames} -seed {seed}')

# Gradio界面
iface = gr.Interface(
    fn=run_inference, 
    inputs=[
        gr.components.Dropdown(params['models'], label='Model'), 
        gr.components.Textbox(value=params['prompt'], label='Prompt'), 
        gr.components.Textbox(value=params['negative'], label='Negative'), 
        gr.components.Slider(minimum=10, maximum=100, step=1, value=params['num_steps'], label='Num Steps'), 
        gr.components.Slider(minimum=10, maximum=100, step=1, value=params['guidance_scale'], label='Guidance Scale'), 
        gr.components.Slider(minimum=128, maximum=1024, step=8, value=params['width'], label='width'), 
        gr.components.Slider(minimum=128, maximum=1024, step=8, value=params['height'], label='height'), 
        # gr.components.Number(value=params['width'], label='Width'), 
        # gr.components.Number(value=params['height'], label='Height'), 
        gr.components.Slider(minimum=1, maximum=60, step=1, value=params['fps'], label='FPS'), 
        gr.components.Slider(minimum=10, maximum=100, step=1, value=params['num_frames'], label='Num Frames'), 
        gr.components.Textbox(value=params['inputSeed'], label='Seed')
    ], 
    outputs=gr.components.Textbox(),
    # layout='vertical',
    # allow_flagging='never'
    )

iface.launch()