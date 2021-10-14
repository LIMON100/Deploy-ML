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

  go to startup application
  
  click add
  
    1. give name
    
    2. set path/location write python full path /home/name/anaconda/python3 /full path
    
    3. starts python script on OS boot 
    
    




