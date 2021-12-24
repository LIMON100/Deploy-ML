#     ########### settings ############
# WIFI_EN_PIN = 8
# # AUDIO_PA_EN_PIN = None  # Bit Dock and old MaixGo
# AUDIO_PA_EN_PIN = 32      # Maix Go(version 2.20)
# # AUDIO_PA_EN_PIN = 2     # Maixduino

# def lcd_show_except(e):
#     err_str = uio.StringIO()
#     sys.print_exception(e, err_str)
#     err_str = err_str.getvalue()
#     img = image.Image(size=(224,224))
#     img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
#     lcd.display(img)

# def main(labels = None, model_addr=0x500000, sensor_window=(224, 224), lcd_rotation=3, sensor_hmirror=False, sensor_vflip=False):
#     sensor.reset()
#     sensor.set_pixformat(sensor.RGB565)
#     sensor.set_framesize(sensor.QVGA)
#     sensor.set_windowing(sensor_window)
#     sensor.set_hmirror(sensor_hmirror)
#     sensor.set_vflip(sensor_vflip)
#     sensor.run(1)

#     sw_count = 0
    
#     # disable wifi
#     fm.register(WIFI_EN_PIN, fm.fpioa.GPIO0, force=True)
#     wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
#     wifi_en.value(0)

#     # open audio PA
#     if AUDIO_PA_EN_PIN:
#         fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
#         wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
#         wifi_en.value(1)

#     # register i2s(i2s0) pin
#     fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
#     fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
#     fm.register(33, fm.fpioa.I2S0_WS, force=True)

#     # init i2s(i2s0)
#     wav_dev = I2S(I2S.DEVICE_0)

#     # init audio
#     player = audio.Audio(path="6.wav")
#     player.volume(100)

#     # read audio info
#     wav_info = player.play_process(wav_dev)
#     print("wav file head information: ", wav_info)

#     # config i2s according to audio info
#     wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
#                            cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
#     wav_dev.set_sample_rate(wav_info[1])


#     lcd.init(type=1)
#     lcd.rotation(lcd_rotation)
#     lcd.clear(lcd.WHITE)

#     if not labels:
#         with open('labels.txt','r') as f:
#             exec(f.read())
#     if not labels:
#         print("no labels.txt")
#         img = image.Image(size=(320, 240))
#         img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
#         lcd.display(img)
#         return 1
#     try:
#         img = image.Image("startup.jpg")
#         lcd.display(img)
#     except Exception:
#         img = image.Image(size=(320, 240))
#         img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
#         lcd.display(img)

#     try:
#         task = None
#         task = kpu.load(model_addr)
#         while(True):
#             img = sensor.snapshot()
#             t = time.ticks_ms()
#             fmap = kpu.forward(task, img)
#             t = time.ticks_ms() - t
#             plist=fmap[:]
#             #print (plist)
#             pmax=max(plist)
#             max_index=plist.index(pmax)
#             img.draw_string(0,0, "%.2f : %s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
#             img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
#             lcd.display(img)

#             if labels[max_index].strip()=="sidewalk":
#                 sw_count = sw_count+1
#                 if sw_count ==20:
#                     sw_count = 0
#                     # init audio
#                     player = audio.Audio(path="/sd/6.wav")
#                     player.volume(100)
#                     # read audio info
#                     wav_info = player.play_process(wav_dev)
#                     print("wav file head information: ", wav_info)

#                     # config i2s according to audio info
#                     wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
#                                            cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
#                     wav_dev.set_sample_rate(wav_info[1])

#                     # loop to play audio
#                     while True:
#                         ret = player.play()
#                         if ret == None:
#                             print("format error")
#                             break
#                         elif ret == 0:
#                             print("end")
#                             break
#                     player.finish()

#     except Exception as e:
#         raise e
#     finally:
#         if not task is None:
#             kpu.deinit(task)


# if __name__ == "__main__":
#     try:
#         labels = ["road","sidewalk","bike-lane","bike-symbol","lama"] # flipped the labels from original code
#         main(labels=labels, model_addr=0x500000)
#         #main(labels=labels, model_addr="/sd/m.kmodel")
#     except Exception as e:
#         sys.print_exception(e)
#         lcd_show_except(e)
#     finally:
#         gc.collect()



import gc, sys
from fpioa_manager import *
from Maix import I2S, GPIO
import audio
import uio



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
#task = kpu.load("/sd/custom_model.kmodel")
task = kpu.load(0x500000)
a = kpu.set_outputs(task, 0, 7,7,50)
anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
#anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
clock=time.clock()

sw_count = 0


WIFI_EN_PIN = 8
# AUDIO_PA_EN_PIN = None  # Bit Dock and old MaixGo
AUDIO_PA_EN_PIN = 32      # Maix Go(version 2.20)
# AUDIO_PA_EN_PIN = 2     # Maixduino


# disable wifi
fm.register(WIFI_EN_PIN, fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

# open audio PA
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
    wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)

# register i2s(i2s0) pin
fm.register(34, fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S0_SCLK, force=True)
fm.register(33, fm.fpioa.I2S0_WS, force=True)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)

while(True):
    clock.tick()
    img = sensor.snapshot().rotation_corr(z_rotation=0.0)
    a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)
    if code:
        fps= clock.fps()
        for i in code:
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0))
            a = img.draw_string(i.x(),i.y(), classes[i.classid()]+(" \n %2.1ffps" % (fps)), color=(255,0,0), scale=1)
            print(classes[i.classid()])
        a = lcd.display(img)

        if classes[i.classid()] == "sidewalk":

            print("Inside sidewalk..................")
            sw_count = sw_count+1
            if sw_count ==20:
                sw_count = 0
                    # init audio
                player = audio.Audio(path="6.wav")
                player.volume(100)
                
                # read audio info
                wav_info = player.play_process(wav_dev)
                print("wav file head information: ", wav_info)

                # config i2s according to audio info
                wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
                wav_dev.set_sample_rate(wav_info[1])

                # loop to play audio
                while True:
                    ret = player.play()
                    if ret == None:
                        print("format error")
                        break
                    elif ret == 0:
                        print("end")
                        break
                player.finish()

        else:
            a = lcd.display(img)


a = kpu.deinit(task)