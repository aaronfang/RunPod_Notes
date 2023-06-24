#!/bin/bash

# Clone the repository
if [ ! -d "kohya_ss" ]; then
  git clone --recurse-submodules https://github.com/Akegarasu/lora-scripts
fi

# Navigate into the cloned directory
cd lora-scripts

# Download the file if it doesn't already exist
if [ ! -f "../sd-models/v1-5-pruned.ckpt" ]; then
  wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt -P ../sd-models
fi

# Run run_gui.sh script
./run_gui.sh

# Deactivate the virtual environment
deactivate
