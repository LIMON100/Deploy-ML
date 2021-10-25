## Tensorrt


## Some Problem

### Problem: opencv coredummbed

Check the numpy version. It causes because of higher numpy version. install numpy 1.19.4
       
    pip3 install numpy==1.19.4


### Problem: TLS memory allocation problem

    export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1
