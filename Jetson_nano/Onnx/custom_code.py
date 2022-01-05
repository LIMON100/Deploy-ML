import cv2
import jetson.inference
import jetson.utils

import Jetson.GPIO as GPIO
 
import time 

led_pin = 7

GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH) 

#net = jetson.inference.detectNet(argv=["--model=ssd-mobilenet2.onnx", "--labels=labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes"], threshold=0.5)

net = jetson.inference.detectNet(argv=["--model=/home/mahmudur/Desktop/l1/test-hel/hel-model1/helmet_cus.onnx", "--labels=/home/mahmudur/Desktop/l1/test-hel/hel-model1/labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes"], threshold=0.5)

#camera = jetson.utils.videoSource("/home/mahmudur/Desktop/l1/test-hel/hel2.mp4")# '/dev/video0' for V4L2
#display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
cap = cv2.VideoCapture("hel3.mp4")
cap.set(3, 640)
cap.set(4, 480)

#COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

while True:
	success, img = cap.read()
	imgCuda = jetson.utils.cudaFromNumpy(img)
	detections = net.Detect(imgCuda)
	#img = jetson.utils.cudaToNumpy(imgCuda)

	for detection in detections:
		#print(detection.Left)
		#print(detection.Bottom)	
		x1,y1,x2,y2 = int(detection.Left), int(detection.Top), int(detection.Right), int(detection.Bottom)
		class_name = net.GetClassDesc(detection.ClassID)

		if class_name == 'head':
			cv2.rectangle(img, (x1, y1), (x2, y2), (14, 218, 247), 2)
			cv2.putText(img, "No-Helmet", (x1+5, y1+15), cv2.FONT_HERSHEY_DUPLEX, 0.75, (32, 14, 247), 2)

		else:
			cv2.rectangle(img, (x1, y1), (x2, y2), (19, 141, 117), 2)
			cv2.putText(img, class_name, (x1+5, y1+15), cv2.FONT_HERSHEY_DUPLEX, 0.75, (35, 155, 86), 2)

	
	cv2.imshow("image",img)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()












