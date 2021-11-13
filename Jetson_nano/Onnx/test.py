import jetson.inference
import jetson.utils

import Jetson.GPIO as GPIO
 
import time 

led_pin = 7

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH) 

net = jetson.inference.detectNet(argv=["--model=ssd-mobilenet2.onnx", "--labels=labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes"], threshold=0.5)

camera = jetson.utils.videoSource("Dublin_Scooter_Video.mp4")# '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

c1 = 0

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

	for detection in detections:
		class_name = net.GetClassDesc(detection.ClassID)
		print(f"Detected '{class_name}'")
		
		if class_name == "sidewalk":
			c1 += 1
			#print(c1)
			
			if c1 > 30:
				GPIO.output(led_pin, GPIO.HIGH)
				print("LED is ON..............................................................")
		
		else:
			c1 = 0
			GPIO.output(led_pin, GPIO.LOW)
			print("LED is OFF")

