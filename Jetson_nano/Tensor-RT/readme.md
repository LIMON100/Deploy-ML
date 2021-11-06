## Tensorrt

Models trained with TensorFlow can be deployed on Jetson Nano in two ways one is either use TensorFlow with TensorRT (TF-TRT) or convert the TensorFlow model to UFF (Universal Framework Format) and generate a TensorRT execution engine from that

### Install Tensorrt into AWS(EC2) or local Linux:

Download tensorrt from Nvidia with your cuda compatible version.

#### Unpack and install
    sudo dpkg -i nv-tensorrt-repo-ubuntu1804-cuda11.4-trt8.2.0.6-ea-20210922_1-1_amd64.deb
    sudo apt-key add /var/nv-tensorrt-repo-ubuntu1804-cuda11.4-trt8.2.0.6-ea-20210922_1-1_amd64/7fa2af80.pub
    sudo apt-get update
    sudo apt-get install tensorrt
    
    If using Python 3.x:
    sudo apt-get install python3-libnvinfer-dev
    
    python3-libnvinfer
    sudo apt-get install uff-converter-tf
    sudo apt-get install onnx-graphsurgeon
    
    Verify the installation.
    dpkg -l | grep TensorRT


#### find tensorrt:
    sudo find / -name tensorrt 2> /dev/null

#### trouble importing tensorrt: Sometimes it install properly but cannot import. If this type of problem happened then run below command.
    pip install nvidia-pyindex
    pip install nvidia-tensorrt

       

## Some Problem

### Problem: AttributeError: 'tensorrt.tensorrt.Builder' object has no attribute 'max_workspace_size(problem of tensorrt version 8. downgrade the version)=>

    pip3 install nvidia-tensorrt==7.2.* --index-url https://pypi.ngc.nvidia.com

### Problem: opencv coredummbed

Check the numpy version. It causes because of higher numpy version. install numpy 1.19.4
       
    pip3 install numpy==1.19.4


### Problem: TLS memory allocation problem

    export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1


### Problem: F tensorflow/compiler/tf2tensorrt/stub/nvinfer_stub.cc:49] getInferLibVersion symbol not found. Fatal Python error: Aborted

There is lot to install so check the below link

https://fantashit.com/tensorflow-tensorrt-could-not-load-dynamic-library-libnvinfer-so-5/


### Problem: F tensorflow/core/util/device name utils.cc:92] Check failed: Is JobName(job)=>

    diff --git a/tf_download_and_trt_model.py b/tf_download_and_trt_model.py
    index c5e608c..083f746 100644
    --- a/tf_download_and_trt_model.py
    +++ b/tf_download_and_trt_model.py
    @@ -1,4 +1,4 @@
    -import tensorflow.contrib.tensorrt as trt
    +from tensorflow.python.compiler.tensorrt import trt_convert as trt
     import sys
     import os
     try:
    @@ -19,6 +19,7 @@ print ("Building detection graph from model " + MODEL + "...")
     frozen_graph, input_names, output_names = build_detection_graph(
         config=config_path,
         checkpoint=checkpoint_path,
    +    force_nms_cpu=False,
         score_threshold=0.3,
         #iou_threshold=0.5,
         batch_size=1
