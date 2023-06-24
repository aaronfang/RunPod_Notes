#!/bin/bash

# Clone the repository
if [ ! -d "kohya_ss" ]; then
  git clone https://github.com/bmaltais/kohya_ss.git
fi

# Navigate into the cloned directory
cd kohya_ss

# Download the file if it doesn't already exist
if [ ! -f "../sd-models/v1-5-pruned.ckpt" ]; then
  wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt -P ../sd-models
fi

# Set up the virtual environment
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Update and install dependencies
apt update -y
if ! dpkg -l | grep -q python3-tk; then
  apt install -y python3-tk
fi

# Run setup script
./setup.sh -p

# Deactivate the virtual environment
deactivate
