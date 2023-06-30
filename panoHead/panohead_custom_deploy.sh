#!/bin/bash

# Define directories
WORKSPACE="/workspace"
PANOHEAD_DIR="$WORKSPACE/PanoHead"
DDFA_DIR="$WORKSPACE/3DDFA_V2"

# clone repos and install dependencies
if [ -d "$PANOHEAD_DIR" ]; then
    rm -rf "$PANOHEAD_DIR"
fi
git clone -b dev1 https://github.com/camenduru/PanoHead $PANOHEAD_DIR
apt-get update
apt -y install -qq aria2

# Define download function
download_file() {
    aria2c --console-log-level=error -c -x 16 -s 16 -k 1M "$1" -d "$2" -o "$3"
}

# Download models
download_file "https://huggingface.co/camenduru/PanoHead/resolve/main/ablation-trigridD-1-025000.pkl" "$PANOHEAD_DIR/models" "ablation-trigridD-1-025000.pkl"
download_file "https://huggingface.co/camenduru/PanoHead/resolve/main/baseline-easy-khair-025000.pkl" "$PANOHEAD_DIR/models" "baseline-easy-khair-025000.pkl"
download_file "https://huggingface.co/camenduru/PanoHead/resolve/main/easy-khair-180-gpc0.8-trans10-025000.pkl" "$PANOHEAD_DIR/models" "easy-khair-180-gpc0.8-trans10-025000.pkl"

pip install imgui glfw pyspng mrcfile ninja plyfile trimesh onnxruntime onnx cython opencv-python click dlib tqdm imageio matplotlib scipy

# Clone and build 3DDFA_V2
if [ -d "$DDFA_DIR" ]; then
    rm -rf "$DDFA_DIR"
fi
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

# 检查是否已经安装了ImageMagick
if ! command -v convert &> /dev/null; then
    echo "ImageMagick未安装,正在尝试安装..."
    apt-get install -y imagemagick
fi

# 找到当前目录下的第一张图片
img_file=$(find "$WORKSPACE" -maxdepth 1 \( -name "*.png" -o -name "*.jpeg" -o -name "*.webp" -o -name "*.jpg" \) -print -quit)

if [ -z "$img_file" ]; then
    echo "在 $WORKSPACE 目录中没有找到任何图片"
    exit 1
fi

# 检查图片是否已经是.jpg格式
if [[ $img_file != *.jpg ]]; then
    # 使用ImageMagick的convert命令将图片转换为.jpg格式
    convert "$img_file" test.jpg
else
    # 如果图片已经是.jpg格式，那么复制它并重命名为test.jpg
    cp "$img_file" test.jpg
fi

mv test.jpg "$WORKSPACE/in/"

# prepare input images
# rm -rf "$WORKSPACE/stage/*" "$DDFA_DIR/crop_samples/img/*" "$DDFA_DIR/test/original/*" "$WORKSPACE/output/*"
# cp "$WORKSPACE/in/*" "$DDFA_DIR/test/original"
# Check if the files exist in the directories before deleting
if [ "$(ls -A $WORKSPACE/stage)" ]; then
   rm -rf "$WORKSPACE"/stage/*
fi

if [ "$(ls -A $DDFA_DIR/crop_samples/img)" ]; then
   rm -rf "$DDFA_DIR"/crop_samples/img/*
fi

if [ "$(ls -A $DDFA_DIR/test/original)" ]; then
   rm -rf "$DDFA_DIR"/test/original/*
fi

if [ "$(ls -A $WORKSPACE/output)" ]; then
   rm -rf "$WORKSPACE"/output/*
fi

# Check if the files exist in the input directory before copying
if [ "$(ls -A $WORKSPACE/in)" ]; then
   cp "$WORKSPACE"/in/* "$DDFA_DIR"/test/original/
fi

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