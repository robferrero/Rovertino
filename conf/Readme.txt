Configuration

Edit /etc/webiopi/config :

Locate [SCRIPTS] section, add following line to load your Python script
...
[SCRIPTS]
myproject = /home/pi/myprj/python/script.py
...

Locate [HTTP] section, add following line to tell WebIOPi where to find your HTML resources
...
[HTTP]
doc-root = /home/pi/myprj/html
...
The two steps above are enough to run our app, but we want to limit remote control to the Light only. By default, we can remotely change function and value of all GPIO.


Locate [REST] section, add following lines
...
[REST]
gpio-export = 17
gpio-post-value = true
gpio-post-function = false 
...
gpio-export limits GPIO exported on the REST API (using BCM numbering)
gpio-post-value allows/forbids to remotely change GPIO values (LOW/HIGH)
gpio-post-function allows/forbids to remotely change GPIO function (IN/OUT)