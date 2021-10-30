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
       

## Some Problem

### Problem: opencv coredummbed

Check the numpy version. It causes because of higher numpy version. install numpy 1.19.4
       
    pip3 install numpy==1.19.4


### Problem: TLS memory allocation problem

    export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1


### Problem: F tensorflow/compiler/tf2tensorrt/stub/nvinfer_stub.cc:49] getInferLibVersion symbol not found. Fatal Python error: Aborted

There is lot to install so check the below link

https://fantashit.com/tensorflow-tensorrt-could-not-load-dynamic-library-libnvinfer-so-5/
