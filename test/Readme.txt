Testing

To debug your script and config, you should first run WebIOPi foreground before using the daemon service :

sudo webiopi -d -c /etc/webiopi/config

You can now open your browser to your Raspberry Pi IP at port 8000 (http://raspberrypi:8000/) and control a light/led connected to GPIO 17.

You can then follow the tutorial on macros to learn how to remotely change on and off hours.