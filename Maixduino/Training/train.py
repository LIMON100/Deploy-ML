import shutil
import numpy as np
np.random.seed(111)
import argparse
import os
import time
import sys
import json
import matplotlib
import datetime
import glob
import pandas as pd
import xml.etree.ElementTree as ET

from networks.yolo.frontend import create_yolo, get_object_labels
from networks.classifier.frontend_classifier import create_classifier, get_labels
from networks.segnet.frontend_segnet import create_segnet
from networks.common_utils.convert import Converter

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4'
import tensorflow as tf

tf.get_logger().setLevel('ERROR')

argparser = argparse.ArgumentParser(
    description='Train and validate YOLO_v2 model on any dataset')

argparser.add_argument(
    '-c',
    '--config',
    default="configs/from_scratch.json",
    help='path to configuration file')

import time
start_time = time.time()


withHelmet_cnt_list = []
withoutHelmet_cnt_list = []

helmet_cnt_list = []
chinstrap_cnt_list = []

dataset_location = "Raw_data"
collected_by = "Arun, Limon, Ozgun"

        

def count_no_of_classes_in_dataset(config, path):

    class_list = config['model']['labels']
    det_counter_per_class = {}

    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (member[0].text)

        
            for j in range(len(class_list)):
            
                if class_list[j] == value:
                    c = class_list[j]

            if c in det_counter_per_class:
                det_counter_per_class[c] += 1
            else:
                det_counter_per_class[c] = 1
                    
    print(det_counter_per_class)
    
    
    """
        put no of object into text file and then save into html
    """
    
    file_path_data = "/home/ubuntu/axelerate-train/aXeleRate/saved_training_log_info/" + "no_of_objects.txt"
    file_data = open(file_path_data,"a")

    print('open text file')
    for key, value in det_counter_per_class.items():
        file_data.write('%s:%s\n' % (key, value))

    file_data.close()
            


def files_cnt(dir):
    initial_count = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    return initial_count
                
if not helmet_cnt_list:
    helmet_cnt_list = [0]
    
if not chinstrap_cnt_list:
    chinstrap_cnt_list = [0]
    

def train_from_config(config,project_folder):
    try:
        matplotlib.use('Agg')
    except:
        pass

    #added for compatibility with < 0.5.7 versions
    try:
        input_size = config['model']['input_size'][:]
    except:
        input_size = [config['model']['input_size'],config['model']['input_size']]
    
    # Create the converter
    converter = Converter(config['converter']['type'], config['model']['architecture'], config['train']['valid_image_folder'])
    
    f_html = open("/home/ubuntu/axelerate-train/aXeleRate/saved_training_log_info/train_info.html", "a")
    f_html.write("<pre>" + "<h1>"+ "Data Info" + "</h1>" + "</pre> <br>\n")
    f_html.write("<pre>" + "<h1>"+ "----------------------------------------------------------" + "</h1>" + "</pre> <br>\n")
    
    train_dataset_path = config['train']['train_annot_folder']
    validation_dataset_path = config['train']['valid_annot_folder']
    count_no_of_classes_in_dataset(config, train_dataset_path)
    
    
    dict_info = {"Collected by " : collected_by, "Dataset location " : dataset_location, 
                 "No. of train dataset" : files_cnt(train_dataset_path),
                 "No. of validation dataset" : files_cnt(validation_dataset_path)}


    file_path_data = "/home/ubuntu/axelerate-train/aXeleRate/saved_training_log_info/" + "data_info.txt"
    file_data = open(file_path_data,"a")

    print('open text file')
    for key, value in dict_info.items():
        file_data.write('%s:%s\n' % (key, value))

    file_data.close()

    contents = open(file_path_data,"r")
    
    for lines in contents.readlines():
        f_html.write("<pre>" + "<h3>"+ lines + "</h3>" + "</pre> <br>\n")
    f_html.write("</body></html>")
    
   

    contents = open(file_path_data,"r")
    
    for lines in contents.readlines():
        f_html.write("<pre>" + "<h3>"+ lines + "</h3>" + "</pre> <br>\n")
    f_html.write("</body></html>")
    
    
    
    """
        Read no of object file and save to html
    """
    
    file_object_data = "/home/ubuntu/axelerate-train/aXeleRate/saved_training_log_info/" + "no_of_objects.txt"
    
    contents = open(file_object_data,"r")
    
    for lines in contents.readlines():
        f_html.write("<pre>" + "<h3>"+ lines + "</h3>" + "</pre> <br>\n")
    f_html.write("</body></html>")
    
    
    
    #  Segmentation network
    if config['model']['type']=='SegNet':
        print('Segmentation')           
        # 1. Construct the model 
        segnet = create_segnet(config['model']['architecture'],
                                   input_size,
                                   config['model']['n_classes'],
                                   config['weights']['backend'])   
        # 2. Load the pretrained weights (if any) 
        segnet.load_weights(config['weights']['full'], by_name=True)
        # 3. actual training 
        model_layers, model_path = segnet.train(config['train']['train_image_folder'],
                                           config['train']['train_annot_folder'],
                                           config['train']['actual_epoch'],
                                           project_folder,
                                           config["train"]["batch_size"],
                                           config["train"]["augumentation"],
                                           config['train']['learning_rate'], 
                                           config['train']['train_times'],
                                           config['train']['valid_times'],
                                           config['train']['valid_image_folder'],
                                           config['train']['valid_annot_folder'],
                                           config['train']['first_trainable_layer'],
                                           config['train']['ignore_zero_class'],
                                           config['train']['valid_metric'])
               
    #  Classifier
    if config['model']['type']=='Classifier':
        print('Classifier')           
        if config['model']['labels']:
            labels = config['model']['labels']
        else:
            labels = get_labels(config['train']['train_image_folder'])
                 # 1. Construct the model 
        classifier = create_classifier(config['model']['architecture'],
                                       labels,
                                       input_size,
                                       config['model']['fully-connected'],
                                       config['model']['dropout'],
                                       config['weights']['backend'],
                                       config['weights']['save_bottleneck'])  
        
        # 2. Load the pretrained weights (if any) 
        classifier.load_weights(config['weights']['full'], by_name=True)

        # 3. actual training 
        model_layers, model_path = classifier.train(config['train']['train_image_folder'],
                                               config['train']['actual_epoch'],
                                               project_folder,
                                               config["train"]["batch_size"],
                                               config["train"]["augumentation"],
                                               config['train']['learning_rate'], 
                                               config['train']['train_times'],
                                               config['train']['valid_times'],
                                               config['train']['valid_image_folder'],
                                               config['train']['first_trainable_layer'],
                                               config['train']['valid_metric'])

    
    

    #  Detector
    if config['model']['type']=='Detector':
        if config['train']['is_only_detect']:
            labels = ["object"]
        else:
            if config['model']['labels']:
                labels = config['model']['labels']
            else:
                labels = get_object_labels(config['train']['train_annot_folder'])
        print(labels)

        # 1. Construct the model 
        yolo = create_yolo(config['model']['architecture'],
                           labels,
                           input_size,
                           config['model']['anchors'],
                           config['model']['coord_scale'],
                           config['model']['class_scale'],
                           config['model']['object_scale'],
                           config['model']['no_object_scale'],
                           config['weights']['backend'])
        
        # 2. Load the pretrained weights (if any) 
        yolo.load_weights(config['weights']['full'], by_name=True)

        # 3. actual training 
        model_layers, model_path = yolo.train(config['train']['train_image_folder'],
                                           config['train']['train_annot_folder'],
                                           config['train']['actual_epoch'],
                                           project_folder,
                                           config["train"]["batch_size"],
                                           config["train"]["augumentation"],
                                           config['train']['learning_rate'], 
                                           config['train']['train_times'],
                                           config['train']['valid_times'],
                                           config['train']['valid_image_folder'],
                                           config['train']['valid_annot_folder'],
                                           config['train']['first_trainable_layer'],
                                           config['train']['valid_metric'])
    
    
    log_file_name = "training_info"
    date = datetime.datetime.now()
    author_name = "limon"
    dataset_link = config['train']['train_annot_folder']
    dataset_link2 = os.path.normpath(dataset_link[0:-18])
    machine_name = "Aws Ec2"
    model_architecture = config['model']['architecture']
    alpha = 1.0
    
    if model_architecture == "MobileNet5_0":
        model_architecture = model_architecture[:-3]
        alpha = 0.50
    elif model_architecture == "MobileNet7_5":
        model_architecture = model_architecture[:-3]
        alpha = 0.75
    elif model_architecture == "MobileNet2_5":
        model_architecture = model_architecture[:-3]
        alpha = 0.25
    elif model_architecture == "MobileNet1_0":
        model_architecture = model_architecture[:-3]
        alpha = 1.0
        
    anchors = config['model']['anchors']
    input_size = config['model']['input_size']
    epochs = config['train']['actual_epoch']
    class_name = config['model']['labels']
    coord_scale = config['model']['coord_scale']
    batch_size = config["train"]["batch_size"]
    valid_metric = config["train"]["valid_metric"]
    learning_rate = config["train"]["learning_rate"]
    optimizer = "Adam(learning_rate=" + str(learning_rate) + ", " + "beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)"
    time_to_finish = (time.time() - start_time) / 60.0

    dict_info = {"Date ": date, "Author name ": author_name, "Machine name ": machine_name, "Dataset path ": dataset_link2,
     "Model architecture ": model_architecture, "Alpha value ": alpha, "Anchors ": anchors, "Input size ": input_size, 
     "Coord scale ": coord_scale, 
     "Epochs ": epochs, "Class name ": class_name, "Batch size ": batch_size,
     "Valid metric ": valid_metric, "Learning rate ": learning_rate, 
      "Optimizer ": optimizer, "Finish time ": (str(time_to_finish) + " " + "Min")}

    file_path = "/home/ubuntu/axelerate-train/aXeleRate/saved_training_log_info/" + log_file_name + ".txt"
    file = open(file_path,"w")

    for key, value in dict_info.items():
        file.write('%s:%s\n' % (key, value))

    file.close()
    
    contents = open(file_path,"r")
    #with open("/home/ubuntu/axelerate-yolov3/aXeleRate/saved_training_log_info/train_info.html", "w") as e:
    f_html.write("<pre>" + "<h1>"+ "Training Info" + "</h1>" + "</pre> <br>\n")
    f_html.write("<pre>" + "<h1>"+ "----------------------------------------------------------" + "</h1>" + "</pre> <br>\n")
    for lines in contents.readlines():
        #e.write("<pre>" + lines + "</pre> <br>\n")
        f_html.write("<pre>" + "<h3>"+ lines + "</h3>" + "</pre> <br>\n")
        
    
    file_path_map = "/home/ubuntu/axelerate-train/aXeleRate/saved_training_log_info/" + "save_map.txt"

    contents = open(file_path_map,"r")
    
    for lines in contents.readlines():
        f_html.write("<pre>" + "<h3>"+ lines + "</h3>" + "</pre> <br>\n")
    f_html.write("</body></html>")
    #file_data.close()
    
  
    
    # 4 Convert the model
    time.sleep(2)

    converter.convert_model(model_path)
    return model_path

def setup_training(config_file=None, config_dict=None):
    """make directory to save weights & its configuration """
    if config_file:
        with open(config_file) as config_buffer:
            config = json.loads(config_buffer.read())
    elif config_dict:
        config = config_dict
    else:
        print('No config found')
        sys.exit()
    dirname = os.path.join("projects", config['train']['saved_folder'])
    if os.path.isdir(dirname):
        print("Project folder {} already exists. Creating a folder for new training session.".format(dirname))
    else:
        print("Project folder {} is created.".format(dirname, dirname))
        os.makedirs(dirname)

    return(train_from_config(config, dirname))


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(
        description='Train and validate YOLO_v2 model on any dataset')

    argparser.add_argument(
        '-c',
        '--config',
        default="configs/classifer.json",
        help='path to configuration file')

    args = argparser.parse_args()
    setup_training(config_file=args.config)
    shutil.rmtree("logs", ignore_errors=True)
