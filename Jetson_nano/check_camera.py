import cv2
import jetson.inference
import jetson.utils
from PIL import Image
import io


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold = 0.5)

def show_camera():

    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        
        
        print("Window open........................")
        
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            
            print("Inside loop........................")

            success, img = cap.read()
            
            
            #b64decoded = base64.b64decode(image)
            #image = Image.open(io.BytesIO(b64decoded))
            #image_np = np.array(image)
            #imgCuda = jetson.utils.cudaFromNumpy(image_np)
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA).astype(np.float32)
            
            img = jetson.utils.cudaFromNumpy(img)
            
            detections = net.Detect(img, 1280, 720)
            
            img = jetson.utils.cudaToNumpy(img, 1280, 720, 4)
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB).astype(np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            #imgCuda = jetson.utils.cudaFromNumpy(img)
            
            #detections = net.Detect(imgCuda)
            
            #img = jetson.utils.cudaToNumpy(imgCuda)
            
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            
            #for d in detections:
             #   x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
              #  className = net.GetClassDesc(d.ClassID)
              #  cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
               # cv2.putText(img, className, (x1+5, y1+15), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 255), 2)
                
            #img = jetson.utils.cudaToNumpy(imgCuda)
            keyCode = cv2.waitKey(30) & 0xFF
            if keyCode == 27:
                break
            
        cap.release()
        cv2.destroyAllWindows()
      
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
