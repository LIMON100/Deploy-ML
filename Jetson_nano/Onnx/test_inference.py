import jetson.inference
import jetson.utils

import Jetson.GPIO as GPIO
 
import time 

led_pin = 7

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH) 

net = jetson.inference.detectNet(argv=["--model=ssd-mobilenet2.onnx", "--labels=labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes"], threshold=0.5)

camera = jetson.utils.videoSource("/home/mahmudur/Desktop/l1/test2/test_video/t1.mkv")# '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

	for detection in detections:
		class_name = net.GetClassDesc(detection.ClassID)
		print(f"Detected '{class_name}'")
		
		if class_name == "sidewalk":
			print("LIMON..................................")
			GPIO.output(led_pin, GPIO.HIGH)
			print("LED is ON")
