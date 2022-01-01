import image

import sensor,image,lcd,time
import KPU as kpu
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)

classes = ["road","sidewalk","bike-lane","bike-symbol","lama"]
#task = kpu.load("/sd/da.kmodel")
task = kpu.load(0x500000)

a = kpu.set_outputs(task, 0, 7,7,50)

anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)

a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

clock=time.clock()

save_count = 0
save_dir = "sav"
results = []

path = "/sd/images2/13.jpg"

#img = image.Image("/sd/images2/15.jpg")
img = image.Image(path)
#img_name = img[:-1]
#print(img_name)

a = img.pix_to_ai()

code = kpu.run_yolo2(task, img)

filename = path.split('/')[-1]

if code:
    print("if")
    fps= clock.fps()

    for i in code:
        print("for")
        a=img.draw_rectangle(i.rect(),color = (0, 255, 0))
        a = img.draw_string(i.x(),i.y(), classes[i.classid()]+(" \n %2.1ffps" % (fps)), color=(255,0,0), scale=1)

        results = []

        #result = {
                   ##'image_id': imagess_ids,
                   #'score': i.value(),
                   #'class': classes[i.classid()],
                   #'xmin': i.w(),
                   #'ymin': i.h(),
                   #'xmax': i.x(),
                   #'ymax': i.y()
                 #}

        results.append(filename)
        results.append(i.value())
        results.append(classes[i.classid()])
        results.append(i.w())
        results.append(i.h())
        results.append(i.x())
        results.append(i.y())



        f = open("/sd/c3.txt", "a")
        f.write(",".join(map(lambda x: str(x), results)))
        f.write('\n')
        f.close()

    a = lcd.display(img)

    #f_name = "{}/{}/{}.jpg".format(images_dir, save_dir, save_count)
    path = "/sd/img4/" + str(save_count) + ".jpg"
    print(path)
    img.save(path)
    save_count += 1

else:
    a = lcd.display(img)

a = kpu.deinit(task)
