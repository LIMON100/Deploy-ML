# Maixduino

### Download 
    Maixpy IDE
    KFLASH_GUI



1. Flash the board

2. Download micorpython firmware (https://dl.sipeed.com/shareURL/MAIX/MaixPy/release/master/maixpy_v0.6.2_72_g22a8555b5)

3. Configure with kFlash

4. Go to maixpy Ide -> Tools -> select-board -> Select Sipped Maixduino


## Train .kmodel with Yolo/SSD

    pip install git+https://github.com/AIWintermuteAI/aXeleRate

    git clone https://github.com/AIWintermuteAI/aXeleRate.git



Go to config folder and choose one json file and change the image train +val directory

    onfigs/custom_file.json
    
    python3 axelerate/train.py -c configs/custom_model.json


## Convert .onnx model to .kmodel


## Convert pytorch model to .kmodel


# Problem:

## xml.etree.elementtree.parseerror: syntax error: line 1, column 0

### Solution

    1. Check the label name put correctly
    2. Check the annotation label is correct
