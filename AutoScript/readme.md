## Write autoscript for different systems.


## Windows:

create two files

1- .bat
  
    @echo off

    python full file path

    @pause / exit




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
    
    




