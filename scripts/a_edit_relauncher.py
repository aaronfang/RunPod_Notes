# replace text in file
def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(old_text, new_text)
    with open(file_path, 'w') as file:
        file.write(content)

file_path = '/workspace/stable-diffusion-webui/relauncher.py'
old_text = 'while True:'
new_text = 'while (n<1):'

replace_text_in_file(file_path, old_text, new_text)

print("========== relauncher.py modified. Please Restart Pod...========== \n")