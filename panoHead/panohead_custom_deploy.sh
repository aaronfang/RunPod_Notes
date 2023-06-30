#!/bin/bash

# Define directories
WORKSPACE="/workspace"
PANOHEAD_DIR="$WORKSPACE/PanoHead"
DDFA_DIR="$WORKSPACE/3DDFA_V2"

# clone repos and install dependencies
git clone -b dev1 https://github.com/camenduru/PanoHead $PANOHEAD_DIR
apt -y install -qq aria2

# Define download function
download_file() {
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M "$1" -d "$2" -o "$3"
}

# Download models
download_file "https://huggingface.co/camenduru/PanoHead/resolve/main/ablation-trigridD-1-025000.pkl" "$PANOHEAD_DIR/models" "ablation-trigridD-1-025000.pkl"
download_file "https://huggingface.co/camenduru/PanoHead/resolve/main/baseline-easy-khair-025000.pkl" "$PANOHEAD_DIR/models" "baseline-easy-khair-025000.pkl"
download_file "https://huggingface.co/camenduru/PanoHead/resolve/main/easy-khair-180-gpc0.8-trans10-025000.pkl" "$PANOHEAD_DIR/models" "easy-khair-180-gpc0.8-trans10-025000.pkl"

pip install imgui glfw pyspng mrcfile ninja plyfile trimesh onnxruntime onnx

# Clone and build 3DDFA_V2
git clone -b dev https://github.com/camenduru/3DDFA_V2 $DDFA_DIR
cd $DDFA_DIR
sh ./build.sh

# Copy files to 3DDFA_V2 directory
cp -rf "$PANOHEAD_DIR/3DDFA_V2_cropping/test" "$DDFA_DIR"
cp "$PANOHEAD_DIR/3DDFA_V2_cropping/dlib_kps.py" "$DDFA_DIR"
cp "$PANOHEAD_DIR/3DDFA_V2_cropping/recrop_images.py" "$DDFA_DIR"

# Download shape_predictor
download_file "https://huggingface.co/camenduru/shape_predictor_68_face_landmarks/resolve/main/shape_predictor_68_face_landmarks.dat" "$DDFA_DIR" "shape_predictor_68_face_landmarks.dat"

# Prepare directories
mkdir -p "$WORKSPACE/in" "$WORKSPACE/stage" "$WORKSPACE/output"

# prepare input images
rm -rf "$WORKSPACE/stage/*" "$DDFA_DIR/crop_samples/img/*" "$DDFA_DIR/test/original/*" "$WORKSPACE/output/*"
cp "$WORKSPACE/in/*" "$DDFA_DIR/test/original"

cd $DDFA_DIR
python dlib_kps.py
python recrop_images.py -i data.pkl -j dataset.json
cp -rf "$DDFA_DIR/crop_samples/img/*" "$WORKSPACE/stage"

# Modify the max_batch in projector_withseg.py and run it
sed -i 's/max_batch = .*/max_batch = 3000000/g' "$PANOHEAD_DIR/projector_withseg.py"
cd $PANOHEAD_DIR
python projector_withseg.py --num-steps=300 --num-steps-pti=300 --shapes=True --outdir="$WORKSPACE/output" --target_img="$WORKSPACE/stage" --network="$PANOHEAD_DIR/models/easy-khair-180-gpc0.8-trans10-025000.pkl" --idx 0

# Run gen_videos_proj_withseg.py for pre and post videos
for video_type in pre post
do
    python gen_videos_proj_withseg.py --output="$WORKSPACE/output/easy-khair-180-gpc0.8-trans10-025000.pkl/0/PTI_render/$video_type.mp4" --latent="$WORKSPACE/output/easy-khair-180-gpc0.8-trans10-025000.pkl/0/projected_w.npz" --trunc 0.7 --network "$WORKSPACE/output/easy-khair-180-gpc0.8-trans10-025000.pkl/0/fintuned_generator.pkl" --cfg Head
done