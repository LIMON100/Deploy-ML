# Works up to 40 images
# reads image 1 by 1 and then stores the bounding boxes in an array
# then loads the image again and draws the bounding boxes
# displays on LCD
# this program crashes because of GC momory issue when it encounters an image
# nothing is detected and the kpu.run_yolo2 returns none. It increases the momory usage
# We can store the kpu.run_yolo2 return results in a text file and then later
# read it and draw it. It should improve program performance
# Before running the program set the GC heap size to 512kb
import machine
import Maix
from Maix import utils

gc_mem_size = 1024*1024

print('config micropython gc stack 1M (1024KB) if not')
if Maix.utils.gc_heap_size() != gc_mem_size:

    Maix.utils.gc_heap_size(gc_mem_size)
    print('updates take effect when you reboot the system. ')
    machine.reset()

print('Current: ', Maix.utils.gc_heap_size())

import image, lcd
import Maix
import image,time,os
import KPU as kpu
import gc, sys
import machine
import time
import uos
import os



#lcd.init(freq=15000000)

#classes = ["road","sidewalk"]
#classes = ["With Helmet","Without Helmet"]
classes = ["With Helmet","Without Helmet","Helmet", "Chin_Strap"]
#task = kpu.load("/sd/sidewalkyolo.kmodel")
task = kpu.load(0x500000)

#a = kpu.set_outputs(task, 0, 7,10,35) #mobilenet
#a = kpu.set_outputs(task, 0, 7,7,50)
a = kpu.set_outputs(task, 0, 7,7,35)
#a = kpu.set_outputs(task, 0, 7,7,21) #yolov3

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

a = kpu.init_yolo2(task, 0.6, 0.3, 5, anchor)
clock=time.clock()
results = []
source = "/sd/hc224" #source224 test224 good_images_part-1 himages
temp = "/sd/temp"
dest = "/sd/destination" #destination test-dest
out = "/sd/out-txt"
max_count = 31 # 999 699 499 299 2040
start_count = 0
results2 = []

#not supported 1
f_html=open("/sd/destination/output_images_chin_strap_v0.0.3.html", "a")

def write_text_to_html():

    message2='''
    <html>
    <head>
    <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            }

            td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            }

            tr:nth-child(even) {

            }
        </style>
    </head>
    <body>
        <h2>Information</h2>
        <table>

    '''

    f_html.write(message2)

def generate_text_file_for_log():

    log_file_name = "log_information"
    date = "22-04-2022"
    author_name = "limon"
    machine_name = uos.uname()[3]
    firmware = "maixpy_v0.6.2_72_g22a8555b5_minimum_with_kmodel_v4_support.bin"
    model_version = "kmodlV4"
    anchors = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    model_size = "1.81 MB"

    dict_info = {"Date": date, "Author name": author_name, "Machine name": machine_name, "Firmware": firmware, "Model version": model_version, "Anchors": anchors, "Model sizee": model_size}

    file_path = "/sd/" + log_file_name + ".txt"
    file = open(file_path,"w")

    for key, value in dict_info.items():
        file.write('%s:%s\n' % (key, value))

    file.close()

    file_path = "/sd/" + log_file_name + "1" + ".log"
    file = open(file_path,"w")

    for key, value in dict_info.items():
        file.write('%s:%s\n' % (key, value))

    file.close()

    write_text_to_html()

    f_html.write("<tr><th>" + "Date" + "</th>")
    f_html.write("<th>" +str(date) + "</th></tr>")
    f_html.write("<tr><th>" + "Author_name" + "</th>")
    f_html.write("<th>" +str(author_name) + "</th></tr>")
    f_html.write("<tr><th>" + "machine_name" + "</th>")
    f_html.write("<th>" +str(machine_name) + "</th></tr>")
    f_html.write("<tr><th>" + "firmware" + "</th>")
    f_html.write("<th>" +str(firmware) + "</th></tr>")
    f_html.write("<tr><th>" + "model_version" + "</th>")
    f_html.write("<th>" +str(model_version) + "</th></tr>")
    f_html.write("<tr><th>" + "anchors" + "</th>")
    f_html.write("<th>" +str(anchors) + "</th></tr>")
    f_html.write("<tr><th>" + "Confidence level" + "</th>")
    f_html.write("<th>" +str(0.6) + "</th></tr>")
    f_html.write("<tr><th>" + "Non-max suppresion(nms)" + "</th>")
    f_html.write("<th>" +str(0.3) + "</th></tr>")
    f_html.write("<tr><th>" + "model_size" + "</th>")
    f_html.write("<th>" +str(model_size) + "</th></tr>")

    f_html.write("</table>")


def save_detection_info(filename, i):
    file_path = "/sd/" + "bounding_boxes_with_filename" + ".txt"
    f = open(file_path, "a")
    f.write(filename)
    f.write("\n")

    detection_info = {"x": i.x(), "y": i.y(), "w": i.w(), "h:": i.h(), "value": i.value(), "classid": i.classid(), "no. of object": i.objnum()}

    for key, value in detection_info.items():
        f.write('%s: %s' % (key, value))
    f.write("\n")
    f.close()

#f_html=open("/sd/test-dest/output_images.html", "a")

def make_html():

    message='''
    <html>
    <head>
        <style type="text/css">
        .gallery li {
        display: inline;
        list-style: none;
        width: 150px;
        min-height: 175px;
        float: left;
        margin: 0 10px 10px 0;
        text-align: center;
        }
        </style>
    </head>
    <body>
        <h2>Predicted Images</h2>
        <table>
            <tr>
              <th>Img No. &nbsp &nbsp</th>
              <th>Bounding Box Coordinates &nbsp &nbsp </th>
              <th>Bounding Box width height &nbsp &nbsp </th>
              <th>No. of classes  &nbsp &nbsp</th>
              <th>Confidence level &nbsp &nbsp</th>
              <th>Image &nbsp &nbsp &nbsp &nbsp</th>
            </tr>

    '''

    f_html.write(message)



def view_free_memory(msg):
    print("Msg: ",msg,"- GC Mem:",gc.mem_free() / 1024,"Heap mem: {}", Maix.utils.heap_free() / 1024) # stack mem

def main():
    generate_text_file_for_log()
    image_count=start_count

    road_class = 0
    sidewalk_class = 0
    none_class = 0

    while(True):
        if image_count > max_count:
            break
        else:
            filename = source + "/" + str(image_count) + ".jpg"
            filename2 = filename.split('/')[-1]
            filename3 = filename2.split('.')[-2]
            #print(filename)
            view_free_memory("Before Img Load to FB")
            img = image.Image(filename).to_rgb565(copy_to_fb=True)
            #lcd.display(img)
            #print("load the picture")
            a = img.pix_to_ai()

            view_free_memory("After pic to AI")
            code = kpu.run_yolo2(task, img)
            results.append (code)
            #print(results[0][2])

            gc.collect()

            if code:
                #print(filename)
                for i in code:
                    #print(i)
                    #print("x= {}, y={}, class={}",i.x(),i.y(), classes[i.classid()])
                    save_detection_info(filename2, i)
                    #print(classes[i.classid()])

                    results2 = []
                    left = int(i.x())
                    top = int(i.y())
                    right = int(left + i.w())
                    bottom = int(top + i.h())

                    #if right > 320:
                        #right = 320

                    if classes[i.classid()] == "Helmet":
                        road_class += 1
                        #cls_name = str("With_Helmet")
                        #results2.append(cls_name)

                    elif classes[i.classid()] == "Chin_Strap":
                        sidewalk_class += 1
                        #cls_name = str("Without_Helmet")
                        #results2.append(cls_name)


                    results2.append(classes[i.classid()])
                    results2.append(i.value())
                    results2.append(left)
                    results2.append(top)
                    results2.append(right)
                    results2.append(bottom)


                    file_path = "/sd/out-txt/" + filename3 + ".txt"
                    f = open(file_path, "a")
                    f.write(" ".join(map(lambda x: str(x), results2)))
                    f.write('\n')
                    f.close()
            else:
                none_class += 1
                print("No objects detected on",filename)


            del img
            gc.collect()
            #print("In Obj rec loop")
            image_count += 1

    Total_images = image_count
    road_classes = road_class
    sidewalk_classes = sidewalk_class
    No_count = Total_images - road_class - sidewalk_class

    message_cnt = "<pre><h1>" + "Count detected and non detected images" + "</h1></pre> <br>\n"
    f_html.write(message_cnt)

    f_html.write("<table>")

    f_html.write("<tr><th>" + "Total Images" + "</th>")
    f_html.write("<th>" +str(Total_images) + "</th></tr>")

    f_html.write("<tr><th>" + "With Helmet detected" + "</th>")
    f_html.write("<th>" +str(road_classes) + "</th></tr>")

    f_html.write("<tr><th>" + "Without Helmet detected" + "</th>")
    f_html.write("<th>" +str(sidewalk_classes) + "</th></tr>")

    f_html.write("<tr><th>" + "No detection" + "</th>")
    f_html.write("<th>" +str(none_class) + "</th></tr>")

    f_html.write("</table>")

    a = kpu.deinit(task)
    image_count =start_count
    print("End Obj Detect")
    #print (results)
    make_html()
    while(True):
        if image_count > max_count:
            break
        else:
            filename = source + "/" + str(image_count) + ".jpg"
            img = image.Image(filename)
            fps=1
            if results[image_count]:
                #print(results)
                for i in results[image_count]:

                    #new_rect = list(i.rect())

                    #if new_rect[2] > 320:
                        #new_rect[2] = 319
                    #new_rect = list(i.rect())

                    #new_rect[2] = new_rect[2] - new_rect[0]
                    #new_rect[3] = new_rect[3] - new_rect[1]
                    #new_tuple = tuple(new_rect)


                    #new_tuple = tuple(new_rect)

                    #i.objnum()
                    if classes[i.classid()] == "Helmet":
                        a = img.draw_rectangle(i.rect(), color = (0, 255, 0))
                        a = img.draw_string(i.x(),i.y(), classes[i.classid()] + (" \n %2.1fconf" % (i.value())), color=(0,0,0), scale=1)

                    elif classes[i.classid()] == "Chin_Strap":
                        a = img.draw_rectangle(i.rect(), color = (255, 0, 0))
                        a = img.draw_string(i.x(),i.y(), classes[i.classid()] + (" \n %2.1fconf" % (i.value())), color=(0,0,0), scale=1)


                    f_html.write("<tr><th>" + str(image_count) + "</th>")
                    f_html.write("<th>" + "x:" + str(i.x()) + " " + "y:" + str(i.y()) + "</th>")
                    f_html.write("<th>" + "w:" + str(i.w()) + " " + "h:" + str(i.h()) + "</th>")
                    f_html.write("<th>" + str(i.objnum()) + "</th>")
                    f_html.write("<th>" + str(i.value()) + "</th>")
                    f_html.write("<th>" + '<a><img src="'+ str(image_count) + ".jpg"+'"></a>' + "</th>")
                    f_html.write("</tr>")
            else:
                #print("Result empty")
                f_html.write("<tr><th>" + str(image_count) + "</th>")
                f_html.write("<th>" + "N/A" + "</th>")
                f_html.write("<th>" + "N/A" + "</th>")
                f_html.write("<th>" + "N/A" + "</th>")
                f_html.write("<th>" + "N/A" + "</th>")
                f_html.write("<th>" + '<a><img src="'+ str(image_count) + ".jpg"+'"></a>' + "</th>")
                f_html.write("</tr>")

            path2 = dest + "/"  + str(image_count) + ".jpg"
            img.save(path2, quality=95)


            #img = draw_string(img, 2, 200, "Limon", color=lcd.WHITE,scale=1, bg=lcd.RED)

            #f_html.write("<th>" + '<a><img src="'+ str(image_count) + ".jpg"+'"></a>' + "</th>")
            #f_html.write("</tr>")

            message2='<a><img src="'+ str(image_count) + ".jpg"+'"></a>'

            #message='<tr><th>image_count &nbsp</th><th>x: 23 y: 21 &nbsp</th><th>w: 16222 h: 221 &nbsp</th><th>1 &nbsp</th><th>0.8518897 &nbsp </th><th><a><img src="'+ str(image_count) + ".jpg"+'"></a>&nbsp &nbsp</th></tr>'

            #f_html.write(message)
            #lcd.display(img)
            del img
            gc.collect()

            #print("In annotation loop")
            image_count += 1

    #make_html()
    f_html.write("</table>")
    f_html.write("</body></html>")
    f_html.close()
    print("Finish Program")



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.print_exception(e)

    finally:
        gc.collect()


