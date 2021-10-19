# Jetson Nano

## <a href="https://github.com/LIMON100/Deploy-ML/tree/master/Jetson_nano/Tensor-RT">Convert Model to Tensor-RT</a>

#### check camera:
    v4l2-ctl --list-devices

#### camera resolution:
    v4l2-ctl --info -d /dev/video0 --list-formats-ex
    
    
    
#### open-camera:
    vgstcapture-1.0 --orientation=2


check jetpack:
cat /etc/nv_tegra_release


#### cuda version:
    nvcc -V

if version is not showing then go to /usr/local and check what version you have. Then write the below command.

    export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}

    export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

Open ~/.bashrc and go to the last and save upper command.

    nano ~/.bashr
    
    
#### check status: (instead of nvidia-smi)

Two way you can check the status or can monitor the cpu,gpu and memory uses.

    sudo tegrastats
    
The another one is showing the full details of everything.


    sudo -H pip3 install -U jetson-stats
    
After installing jetson-stats run following command to see the status

    jtop


![](https://github.com/LIMON100/Deploy-ML/blob/master/Jetson_nano/images/jetson-stat.PNG?raw=true)


