# Jetson Nano


#### check camera:
    v4l2-ctl --list-devices

#### camera resolution:
    v4l2-ctl --info -d /dev/video0 --list-formats-ex
