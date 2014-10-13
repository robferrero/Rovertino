#Imports
import webiopi
import os
import datetime
import time

# Retrieve GPIO lib
GPIO = webiopi.GPIO

SCRIPTPATH = "."

# GPIO pin using BCM numbering
LIGHT = 22  # prova only 

# DC motor control
#MOSI #10 = x19   
#MISO #09 = x21   
#CE0  #08 = x24
#CE1  #07 = x26
MOTOR_A1 = 7  #MOTORSX2
MOTOR_A2 = 8  #MOTORDX2
MOTOR_B1 = 9  #MOTORSX1
MOTOR_B2 = 10   #MOTORDX1


#proximity IR sensor
SENSOR_SX = 4
SENSOR_DX = 17

#follow line sensor  (Not used for now)
FOLLOW_SX = 18
FOLLOW_DX = 27

FREE5= 22
FREE6= 23

# Panoramica = movimento orizzontale
PAN =24
SERVOPAN = 18 #aka GPIO 24 
# Inclinazione = movimento verticale
TILT = 25
SERVOTILT =  22 #aka GPIO25

servo_PanTilt_pins = [18,22]   # aka GPIO24  GPIO25     rrrr da girare hardware
#servodPins = [0,0]     #valued after initialization  non e' vero 

actual=[150,150]   #init in the middle 
#vvalue limit for MY Pan (servo0) and Tilt (servo1)
min = [60,70]
max = [250,190]
neutral =[150,150]
inc = [10,10]

#ultrasonic
ULTRASONIC = 14

HOUR_ON  = 8  # Turn Light ON at 08:00
HOUR_OFF = 18 # Turn Light OFF at 18:00

# setup function is automatically called at WebIOPi startup
def setup():
    # disable warning for reconfiguration 
    #GPIO.setwarnings(False)
    GPIO.setFunction(LIGHT, GPIO.OUT)
    
    # set the GPIO used by the motor to output
    GPIO.setFunction(MOTOR_A1, GPIO.OUT)
    GPIO.setFunction(MOTOR_A2, GPIO.OUT)
    GPIO.setFunction(MOTOR_B1, GPIO.OUT)
    GPIO.setFunction(MOTOR_B2, GPIO.OUT)
  
    # set the GPIO used by the IR Sensor  to input
    GPIO.setFunction(SENSOR_SX, GPIO.IN)
    GPIO.setFunction(SENSOR_DX, GPIO.IN)
    
    # set the GPIO used by the follow line sensor  to input
    GPIO.setFunction(FOLLOW_SX, GPIO.IN)
    GPIO.setFunction(FOLLOW_DX, GPIO.IN)
    
    # set the GPIO used by the pan/tilt to soft PWM output
    #used through servoblaster
    GPIO.setFunction(PAN, GPIO.OUT)
    GPIO.setFunction(TILT, GPIO.OUT)

    #init servoblaster
    startServod(servo_PanTilt_pins);
    
    # set the GPIO used by the ultrasonic to output
    GPIO.setFunction(ULTRASONIC, GPIO.OUT)
    
    # retrieve current datetime
    now = datetime.datetime.now()

    # test if we are between ON time and tun the light ON
    #if ((now.hour >= HOUR_ON) and (now.hour < HOUR_OFF)):
    #    GPIO.digitalWrite(LIGHT, GPIO.HIGH)

# loop function is repeatedly called by WebIOPi 
def loop():
    # retrieve current datetime
    now = datetime.datetime.now()

    # gestione resto divisione (modulo)    ---->  /10 = 6 volte al minuto    /5 = 12 volte al minuto    /3 = 20 volte al minuto   /2 = 30 volte al minuto 
    if (now.second % 10 == 0):
    #if ((now.second == 10)  or (now.second == 20) or (now.second == 30) or (now.second == 60)  or (now.second == 50) or (now.second == 0)): 
        print ("sonar_queryUltra call " + str(now.second) )
        queryUltra() 

    # toggle light ON all days at the correct time
    #if ((now.hour == HOUR_ON) and (now.minute == 0) and (now.second == 0)):
    #    if (GPIO.digitalRead(LIGHT) == GPIO.LOW):
    #        GPIO.digitalWrite(LIGHT, GPIO.HIGH)

    # toggle light OFF
    #if ((now.hour == HOUR_OFF) and (now.minute == 0) and (now.second == 0)):
    #    if (GPIO.digitalRead(LIGHT) == GPIO.HIGH):
    #        GPIO.digitalWrite(LIGHT, GPIO.LOW)

    # gives CPU some time before looping again
    webiopi.sleep(0.1)

# destroy function is called at WebIOPi shutdown
def destroy():
    print ("exit servod")
    #stop servoblaster
    stopServod()
    
    #GPIO.setFunction(LIGHT, GPIO.IN)
    GPIO.setFunction(MOTOR_A1, GPIO.IN)
    GPIO.setFunction(MOTOR_A2, GPIO.IN)    
    GPIO.setFunction(MOTOR_B1, GPIO.IN)
    GPIO.setFunction(MOTOR_B2, GPIO.IN) 
    GPIO.setFunction(PAN, GPIO.IN)
    GPIO.setFunction(TILT, GPIO.IN)
    GPIO.setFunction(SENSOR_SX, GPIO.IN)
    GPIO.setFunction(SENSOR_DX, GPIO.IN)
    GPIO.setFunction(FOLLOW_SX, GPIO.IN)
    GPIO.setFunction(FOLLOW_DX, GPIO.IN)
    GPIO.setFunction(ULTRASONIC, GPIO.IN)

    
# A macro which says hello
@webiopi.macro
def helloWorld(first, last):
    webiopi.debug("HelloWorld(%s, %s)" % (first, last))
    return "Hello %s %s !" % (first, last)

# A macro without args which return nothing
@webiopi.macro
def printTime():
    webiopi.debug("PrintTime: " + time.asctime())    
    
@webiopi.macro
def getLightHours():
    return "%d;%d" % (HOUR_ON, HOUR_OFF)

@webiopi.macro
def setLightHours(on, off):
    global HOUR_ON, HOUR_OFF
    HOUR_ON = int(on)
    HOUR_OFF = int(off)
    return getLightHours()    

    
@webiopi.macro
def turnLeft():
#accende motori dx avanti
    GPIO.digitalWrite(MOTOR_A1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_A2, GPIO.HIGH)   #dx avanti
    GPIO.digitalWrite(MOTOR_B1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B2, GPIO.LOW)
    return 1;
    
    
@webiopi.macro
def turnRight():
#accendi motori sx avanti
    GPIO.digitalWrite(MOTOR_A1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_A2, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B2, GPIO.HIGH)   #sx avanti 
    return 1;
    
    
@webiopi.macro
def fastLeft():
#accende motori dx avanti sx indietro 
    GPIO.digitalWrite(MOTOR_A1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_A2, GPIO.HIGH)   #dx avanti
    GPIO.digitalWrite(MOTOR_B1, GPIO.HIGH)   #sx indietro
    GPIO.digitalWrite(MOTOR_B2, GPIO.LOW)
    return 1;
    
    
@webiopi.macro
def fastRight():
#accendi motori dx indietro sx avanti
    GPIO.digitalWrite(MOTOR_A1, GPIO.HIGH)   #dx indietro
    GPIO.digitalWrite(MOTOR_A2, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B2, GPIO.HIGH)   #sx avanti 
    return 1;

    
@webiopi.macro
def forward():
#accendi motori sx e dx entrambi avanti
    GPIO.digitalWrite(MOTOR_A1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_A2, GPIO.HIGH)   #dx avanti
    GPIO.digitalWrite(MOTOR_B1, GPIO.LOW)   
    GPIO.digitalWrite(MOTOR_B2, GPIO.HIGH)   #sx avanti 
    return 1;

    
@webiopi.macro
def reverse():
#accendi motori sx e dx entrambi indietro
    GPIO.digitalWrite(MOTOR_A1, GPIO.HIGH)   #dx indietro
    GPIO.digitalWrite(MOTOR_A2, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B1, GPIO.HIGH)   #sx indietro
    GPIO.digitalWrite(MOTOR_B2, GPIO.LOW)
    return 1;   

@webiopi.macro
def backLeft():
#accende motori dx indietro sx avanti (= come fastRight)
    GPIO.digitalWrite(MOTOR_A1, GPIO.HIGH)   #dx indietro
    GPIO.digitalWrite(MOTOR_A2, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B2, GPIO.HIGH)   #sx avanti 
    return 1;
   
@webiopi.macro
def backRight():
#accendi motori dx avanti sx indietro (= come fastLeft)
    GPIO.digitalWrite(MOTOR_A1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_A2, GPIO.HIGH)   #dx avanti
    GPIO.digitalWrite(MOTOR_B1, GPIO.HIGH)   #sx indietro
    GPIO.digitalWrite(MOTOR_B2, GPIO.LOW)
    return 1;
    
    
@webiopi.macro
def stop():
#stop motori sx e dx fermi
    GPIO.digitalWrite(MOTOR_A1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_A2, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B1, GPIO.LOW)
    GPIO.digitalWrite(MOTOR_B2, GPIO.LOW)
    return 1;
    
    
@webiopi.macro
def queryUltra():
    distance = 222
#based on github.com_chrisalexander and ScratchGPIO - https://github.com/cymplecy/scratch_gpio
    GPIO.setFunction(ULTRASONIC, GPIO.OUT)
    ti = time.time()
      
    distlist = [0.0,0.0,0.0]
    ts=time.time()
        
    for k in range(3):
        GPIO.setFunction(ULTRASONIC, GPIO.OUT)
        GPIO.digitalWrite(ULTRASONIC, 1)
        time.sleep(0.00001)
        GPIO.digitalWrite(ULTRASONIC, 0)
        t0=time.time()
        GPIO.setFunction(ULTRASONIC, GPIO.IN)
       
        t1=t0
        while ((GPIO.digitalRead(ULTRASONIC)==0) and ((t1-t0) < 0.02)):
            t1=time.time()

        t1=time.time()
        t2=t1

        while ((GPIO.digitalRead(ULTRASONIC)==1) and ((t2-t1) < 0.02)):
            t2=time.time()
            
        t2=time.time()
        t3=(t2-t1)

        distance=t3*343/2*100
        distlist[k]=distance

    GPIO.setFunction(ULTRASONIC, GPIO.OUT)
    tf = time.time() - ts
	
    distance = sorted(distlist)[1]
      
    if (distance > 280):
        distance = 299
    if (distance < 2):
        distance = 1

    webiopi.debug("Print Sonar Distance: %d" % distance)
    return "%d" % distance 
    
    
#serve servoblaster per comandare meglio i servo
# input RoVerto servo_PanTilt_pins = [18,22]   # aka GPIO24  GPIO25
def startServod(pins):
    print ("Starting servod")
    os.system("sudo pkill -f servod")
    os.system(SCRIPTPATH +'/servod --idle-timeout=20000 --p1pins="' + str(pins).strip('[]') + '"')
    print (SCRIPTPATH +'/servod --idle-timeout=20000 --p1pins="' + str(pins).strip('[]') + '"')
    servodPins = pins
    pin = SERVOPAN
    os.system("echo " + str(servodPins.index(pin)) + "=" + str(neutral[0]) + " > /dev/servoblaster")
    pin = SERVOTILT
    os.system("echo " + str(servodPins.index(pin)) + "=" + str(neutral[1]) + " > /dev/servoblaster")
    
def pinServod(pin, value):
    print ("echo pin " + str(pin))
    print ("echo value " + str(value))
    print ("echo servo_PanTilt_pins[%d]= %d " % (servo_PanTilt_pins.index(pin) , actual[servo_PanTilt_pins.index(pin)]) )  #questi ci sono ok
    assign = "=+"
    valuedelta = value
    if (value < 0):
        assign = "=-"
        valuedelta = -value
    if ( actual[servo_PanTilt_pins.index(pin)] > min[servo_PanTilt_pins.index(pin)] and actual[servo_PanTilt_pins.index(pin)] < max[servo_PanTilt_pins.index(pin)] ):
        print ("echo " + str(servo_PanTilt_pins.index(pin)) + assign + str(valuedelta) + " > /dev/servoblaster")
        os.system("echo " + str(servo_PanTilt_pins.index(pin)) + assign + str(valuedelta) + " > /dev/servoblaster")
        actual[servo_PanTilt_pins.index(pin)] = actual[servo_PanTilt_pins.index(pin)] + value
        
def stopServod():
    os.system("sudo pkill -f servod")
    
@webiopi.macro    
def PanLeft():
    pin = SERVOPAN
    pinServod(pin,inc[0])
    #value = inc[0]
    #print ("echo value " + str(value))
    #os.system("echo " + "0" + "=+" + str(value) + " > /dev/servoblaster")   # RRR cosi funziona e aumento di 10 ma mancano controlli ed e' come se facesse down -->   0 = tilt  1 = pan  da girare hardware
 
@webiopi.macro    
def PanRight():
    pin = SERVOPAN
    pinServod(pin,-inc[0])

@webiopi.macro    
def TiltUp():
    pin = SERVOTILT
    pinServod(pin,-inc[1])
    
@webiopi.macro    
def TiltDown():
    pin = SERVOTILT
    pinServod(pin,inc[1])

@webiopi.macro    
def PTcenter():
    pin = SERVOPAN
    os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(neutral[0]) + " > /dev/servoblaster")
    actual[servo_PanTilt_pins.index(pin)] = neutral[servo_PanTilt_pins.index(pin)] 
    pin = SERVOTILT
    os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(neutral[1]) + " > /dev/servoblaster")
    actual[servo_PanTilt_pins.index(pin)] = neutral[servo_PanTilt_pins.index(pin)] 
    
@webiopi.macro    
def yes():
    pin = SERVOTILT
    sleepTime = .2
    
    os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(neutral[1]) + " > /dev/servoblaster")
    for i in range(1, 4):
        time.sleep(sleepTime)
        os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(min[1]) + " > /dev/servoblaster")
        time.sleep(sleepTime)
        os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(max[1]) + " > /dev/servoblaster")
    os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(neutral[1]) + " > /dev/servoblaster")
    
@webiopi.macro    
def no():
    pin = SERVOPAN
    sleepTime = .4

    os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(neutral[0]) + " > /dev/servoblaster")
    for i in range(1, 4):
        time.sleep(sleepTime)
        os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(min[0]) + " > /dev/servoblaster")
        time.sleep(sleepTime)
        os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(max[0]) + " > /dev/servoblaster")
    os.system("echo " + str(servo_PanTilt_pins.index(pin)) + "=" + str(neutral[0]) + " > /dev/servoblaster")
