## Write autoscript for different systems.


## Windows:

create two files

1- .bat
  
    @echo off

    python full file path

    @pause / exit
    
      
2- .vbs

    CreateObject("Wscript.Shell").Run "full path of .bat", 0, True



3.go to your python file

    import pywintypes
    
    from win10toast import ToastNotifier
    
    
    
4.write below code before start while loop

    toast = ToastNotifier()
    
    toast.show_toast("File organizer", "The process has been started", duration = 30)
    
    
    os.chdir("python file full path")
    
    
    
    
5. go to registry:
  
    create new string value in run 

    set Value data: full path of .vbs file

    restart computer
    


or goto:

    user->name->appdata->roadming->microsoft->windows->start-menu->programs->startup

    paste the .bat file




## Raspberry Pi:

  sudo crontab -e
  
  @reboot python3 /full path of the file/.py
  
  sudo raspi-config
  
  select the 3.boot option -> b2.control autologin
  
  
#### if have multiple program.
  
  set & sign in last 
  
  exple: python3 home/name/.py &
  
  abc.py


## ubuntu:

### Systemd
  sudo nano /lib/systemd/system/sample.service

  Add in the following text :

  [Unit]
  Description=My Sample Service
  After=multi-user.target

  [Service]
  Type=idle
  ExecStart=/usr/bin/python /home/pi/sample.py

  [Install]
  WantedBy=multi-user.target




  ExecStart=/usr/bin/python /home/pi/sample.py > /home/pi/sample.log 2>&1
  The permission on the unit file needs to be set to 644 :

  sudo chmod 644 /lib/systemd/system/sample.service
  Step 2 – Configure systemd
  Now the unit file has been defined we can tell systemd to start it during the boot sequence :

  sudo systemctl daemon-reload
  sudo systemctl enable sample.service
  Reboot the Pi and your custom service should run:

  sudo reboot

  systemctl status sample.service

  go to startup application
  
  click add
  
    1. give name
    
    2. set path/location write python full path /home/name/anaconda/python3 /full path
    
    3. starts python script on OS boot 
    
    




