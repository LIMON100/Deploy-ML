# Maixduino

### Download  
    Maixpy IDE
    KFLASH_GUI



1. Flash the board

2. Download micorpython firmware (https://dl.sipeed.com/shareURL/MAIX/MaixPy/release/master/maixpy_v0.6.2_72_g22a8555b5)

3. Configure with kFlash

4. Go to maixpy Ide -> Tools -> select-board -> Select Sipped Maixduino


# Object-Detection

## Train .kmodel with Yolo2/SSD

### Setup for 'recall' matric

    pip install git+https://github.com/AIWintermuteAI/aXeleRate

    git clone https://github.com/AIWintermuteAI/aXeleRate.git


### Setup for 'mAP' matric

    pip install axelerate==0.7.0
    
    git clone -b legacy-yolov2 https://github.com/AIWintermuteAI/aXeleRate.git
    
 
#### If pip install cannot install axelerate with brach "legacy-yolov2" then copy all files inside the axelerate->axelerate and paste it where the axelerate installed.


Go to config folder and choose one json file and change the image train +val directory

    onfigs/custom_file.json
    
    python3 axelerate/train.py -c configs/custom_model.json
    
    
Some parameters

    

## Train yolov3/tiny_yolo

    1. For object detection or classification it is good to make a dataset based on the model input size. Different resolution data can be added but it must not exceed (20-25)%.

    2. Put different position and lighting condition datasets.



#### Problem: (ValueError: Empty training data)

#### Solution
    
     Reduce batch_size
     
     Check the train/val folder image size(no_of_images)


### Convert using nncase

#### Problem:

    Conan "No such file or directory"
    
    
### Solution:

    source ~/.profile


### Convert to tflite

### Convert model into kmodel

## Convert .onnx model to .kmodel

    convert to .tflite
    convert tflite to .kmodel


## Convert pytorch model to .kmodel

# Segmentation

# Problem:

## xml.etree.elementtree.parseerror: syntax error: line 1, column 0

### Solution

    1. Check the label name put correctly
    2. Check the annotation label is correct
    3. Check inside annotation folder is there any other file (Sometimes after copy the zip file and unzip it there remains an extra file e.x(desktop.ini))
    

## 'str' object has no attribute 'decode'

    pip install 'h5py==2.10.0' --force-reinstall



# Maixpy Compilation

To install any default firmware go to below link,

Install custom library with firmware

# Problem in compilation

## 1. Permission denied(Attempting to use a port that is not open)

### Solution

    sudo chmod 666 /dev/ttyS0

check available port in the cloud or local
    
    ls /dev
