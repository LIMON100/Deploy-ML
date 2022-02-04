from axelerate import setup_training, setup_inference, setup_evaluation

#model_path = "I:/JumpWatts/Dataset/helmet-detectn/K-model/model2/helmet-keras.h5"

# #%matplotlib inline
# from keras import backend as K 
# K.clear_session()
# setup_inference(config, model_path)

import argparse
import json
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tensorflow.keras import backend as K 
from axelerate.networks.yolo.frontend import create_yolo
from axelerate.networks.yolo.backend.utils.box import draw_boxes
from axelerate.networks.yolo.backend.utils.annotation import parse_annotation
from axelerate.networks.segnet.frontend_segnet import create_segnet
from axelerate.networks.segnet.predict import predict
from axelerate.networks.classifier.frontend_classifier import get_labels, create_classifier
from shutil import copyfile

import os
import glob
import tensorflow as tf

K.clear_session()

DEFAULT_THRESHOLD = 0.3
weights = "I:/JumpWatts/Dataset/helmet-detectn/K-model/model2/helmet-keras.h5" 
    
def show_image(filename):
    image = mpimg.imread(filename)
    plt.figure()
    plt.imshow(image)
    plt.show(block=False)
    plt.pause(1)
    plt.close()
    print(filename)

def create_ann(filename, image, boxes, right_label, label_list):
    copyfile(filename, 'test_img/'+os.path.basename(filename))
    writer = Writer(filename, image.shape[0], image.shape[1])
    for i in range(len(right_label)):
        writer.addObject(label_list[right_label[i]], boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])
    name = os.path.basename(filename).split('.')
    writer.save('test_ann/'+name[0]+'.xml')

def prepare_image(img_path, network):
    orig_image = cv2.imread(img_path)
    input_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) 
    input_image = cv2.resize(input_image, (network._input_size[1],network._input_size[0]))
    input_image = network._norm(input_image)
    input_image = np.expand_dims(input_image, 0)
    return orig_image, input_image

def setup_inference(img_path, img_fname):

    config={
        "model" : {
            "type":                 "Detector",
            "architecture":         "MobileNet7_5",
            "input_size":           224,
            "anchors":              [1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025],
            "labels":               ["With Helmet","Without Helmet"],
            "obj_thresh" : 		    0.7,
            "iou_thresh" : 		    0.5,
            "coord_scale" : 		1.0,
            "class_scale" : 		1.0,
            "object_scale" : 		5.0,
            "no_object_scale" : 	1.0
        },
        "weights" : {
            "full":   				"I:/JumpWatts/Dataset/helmet-detectn/K-model/model2/helmet-keras.h5",
            "backend":              "imagenet"
        },
        "train" : {
            "actual_epoch":         1,
            "train_image_folder":   "/home/ubuntu/helmet-detect/dataset/new-dataset/train2/imgs",
            "train_annot_folder":   "/home/ubuntu/helmet-detect/dataset/new-dataset/train2/annot",
            "train_times":          4,
            "valid_image_folder":   "I:/JumpWatts/Dataset/helmet-detectn/K-model/n1",
            "valid_annot_folder":   "/home/ubuntu/helmet-detect/dataset/new-dataset/valid2/annot",
            "valid_times":          4,
            "valid_metric":         "mAP",
            "batch_size":           4,
            "learning_rate":        1e-4,
            "saved_folder":   		"I:/JumpWatts/Dataset/helmet-detectn/K-model",
            "first_trainable_layer": "",
            "augumentation":		False,
            "is_only_detect" : 		False
        },
        "converter" : {
            "type":   				["k210","tflite"]
        }
    }


    config = config 
    #weights = "I:/JumpWatts/Dataset/helmet-detectn/K-model/model2/helmet-keras.h5" 
    threshold = 0.3
    create_dataset = None

    try:
        matplotlib.use('TkAgg')
    except:
        pass
    #added for compatibility with < 0.5.7 versions
    try:
        input_size = config['model']['input_size'][:]
    except:
        input_size = [config['model']['input_size'],config['model']['input_size']]

    """make directory to save inference results """
    dirname = os.path.join(os.path.dirname(weights),'Inference_results')
    if os.path.isdir(dirname):
        print("Folder {} is already exists. Image files in directory might be overwritten".format(dirname))
    else:
        print("Folder {} is created.".format(dirname))
        os.makedirs(dirname)

    if config['model']['type']=='Detector':
        # 2. create yolo instance & predict
        yolo = create_yolo(config['model']['architecture'],
                           config['model']['labels'],
                           input_size,
                           config['model']['anchors'])
        yolo.load_weights(weights)
        
        #valid_image_folder = config['train']['valid_image_folder']
        #image_files_list = glob.glob(valid_image_folder + '/**/*.jpg', recursive=True)
        #image_files_list = "I:/JumpWatts/Dataset/helmet-detectn/K-model/n1/bar22.jpg"
        #print("take all images.................................################################################################")
        
        inference_time = []

        #for i in range(len(image_files_list)):
        #img_path = image_files_list
        #img_fname = os.path.basename(img_path)

        #print(img_path)
        #print(img_fname)

        orig_image, input_image = prepare_image(img_path, yolo)
        height, width = orig_image.shape[:2]
        prediction_time, boxes, probs = yolo.predict(input_image, height, width, float(threshold))
        inference_time.append(prediction_time)
        labels = np.argmax(probs, axis=1) if len(probs) > 0 else []
            
        # 4. save detection result
        orig_image = draw_boxes(orig_image, boxes, probs, config['model']['labels'])
        output_path = os.path.join(dirname, os.path.split(img_fname)[-1])
        if len(probs) > 0 and create_dataset:
            create_ann(img_path, orig_image, boxes, labels, config['model']['labels'])
        
        print("THE BOX VALUE IS....................................................**********")
        print(boxes[0][0])
        #print(boxes[1])
        #cv2.imwrite(output_path, orig_image)
        output_path2 = 'I:/JumpWatts/axel/for-helmet/static/detections/'
        cv2.imwrite(output_path2 + '{}' .format(img_fname), orig_image)
        print("{}-boxes are detected. {} saved.".format(len(boxes), output_path))
        #show_image(output_path)

        if len(inference_time)>1:
            print("Average prediction time:{} ms".format(sum(inference_time[1:])/len(inference_time[1:])))
