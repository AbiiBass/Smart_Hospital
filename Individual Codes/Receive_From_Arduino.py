#Bluetooth UART receiver for Heart Beat an Temperature data and send to ThingSpeak server 
#Data sending to TS, Send HB Temp alert 
import time                         #import time for delay
import datetime                     #import date and time
import urllib.request               #import urllib to open HTTP url links
import serial                       #encapsulate access for serial ports
import RPi.GPIO as GPIO             #import Raspberry Pi GPIO module as GPIO
GPIO.setwarnings(False)             #disable warnings
GPIO.setmode(GPIO.BCM)              #Set Broadcom SOC channel

buzNlight = 25                      #insert buzzer and LED (buzNlight) to GPIO pin 25
GPIO.setup(buzNlight, GPIO.OUT)     #set GPIO pin 25 as Output

NurseAlert = 23                     #insert LED for Nurse assistance (NurseAlert) to GPIO pin 23
GPIO.setup(NurseAlert, GPIO.OUT)                                    #set GPIO pin 23 as Output

encoding = 'utf-8'                  #Bluetooth UART receive character string encoding 

api_key = "RIVX854RLHS3UEYN"                                        #Write API key for ThingSpeak channel
base_url = "http://api.thingspeak.com/update?api_key=%s" % api_key  #URL link for ThingSpeak page and channel used

uart_channel = serial.Serial("/dev/ttyAMA0", baudrate =9600, timeout=2)     #Enable UART channed ttyAMA0 with baudrate 9600 bps and  time out for 2 sec.
Txdata=0                            #Initlize Transmit data as intiger


HB_TMPdata=""                       #Initlize Heatbeat, Temperature, Nurse Caling data, Patient ID tag as string 
HBdata=""                           #Initlize Heart beat data as string 
TMPdata=""                          #Initlize Temperature Data as string
NCdata=""                           #Initlize Nurse Caling data as string
NameA=""                            #Initlize Patient ID tag as string

HBfloat = 0.0                       #Initlize Heart beat float data as float
TMPfloat = 0.0                      #Initlize Temperature float Data as float
NCint = 0                           #Initlize Nurse Caling data as intiger
Name = 0                            #Initlize Patient ID tag as integer

HAstate = 0                         #Initlize Health Alarm State as integer

    

def LongAlert ():                       # define LongAlert as...
    GPIO.output(buzNlight, True)        ##############################      
    time.sleep(1)                       ##                          ##
    GPIO.output(buzNlight, False)       ##   Buzzer and Led go off  ##     
    time.sleep(2)                       ##          slowly          ##
    GPIO.output(buzNlight, True)        ##                          ##
    time.sleep(1)                       ##   both ON for 1 second   ##
    GPIO.output(buzNlight, False)       ##            and           ##
    time.sleep(2)                       ##   both OFF for 2 second  ##
    HAstate = 1                         ##                          ##
                                        ##############################
    
def ShortAlert ():                      # define ShortAlert as...
    GPIO.output(buzNlight, True)        ##############################      
    time.sleep(0.5)                     ##                          ##
    GPIO.output(buzNlight, False)       ##   Buzzer and Led go off  ##     
    time.sleep(0.2)                     ##          slowly          ##
    GPIO.output(buzNlight, True)        ##                          ##
    time.sleep(0.5)                     ## both ON for 0.5 second   ##
    GPIO.output(buzNlight, False)       ##            and           ##
    time.sleep(0.2)                     ## both OFF for 0.2 second  ##
    HAstate = 2                         ##                          ##
                                        ##############################




uart_channel.reset_input_buffer()       #Reset or clear UART channed ttyAMA0 (HC05) Transmit buffer

while 1:
    Rxdata = uart_channel.readline()    #Clear UART channed ttyAMA0 (HC05) Receive buffer

#           format of data sent from Arduino
#           Heart Beat value & temperature value & Nurse Calling state & Patient ID
# position:         0        &          1        &          2          &    3
    
    try: 
        HB_TMPdata = str (Rxdata, encoding)         #Convert all received data to String with 'utf-8' encoding 
        HBdata = HB_TMPdata.split("&")[0]           #Seperate Heart beat data String before & 
        TMPdata = HB_TMPdata.split("&")[1]          #Seperate Temperature data String before & 
        NCdata = HB_TMPdata.split("&")[2]           #Seperate Nurse calling data String before & 
        NameA = HB_TMPdata.split("&")[3]            #Seperate Patient Tag ID data String before & 
        print (HBdata)                              #Print value of HBdata
        print (TMPdata)                             #Print value of TMPdata
        print (NCdata)                              #Print value of NCdata
        print ("Patient ID: ", NameA)               #Print Patient's tag ID value in this format. Patient ID:__________
    
#       print("Last valid input: " + str(datetime.datetime.now()))

        url = base_url + "&field1=%s" % (HBdata)    #Send Heart beat data to field 1 of thingspeak channel
#       print(url)
        f = urllib.request.urlopen(url)             #set f as request to open URL link for Heart Beat data          
        url = base_url + "&field2=%s" % (TMPdata)   #Send Temperature data to field 2 of thingspeak channel
#        print(url)
        f = urllib.request.urlopen(url)             #set f as request to open URL link for Temperature data 
#       print (f.read())
        f.close()                                   #close the that was already opened
#        print(type(HBdata))
        HBfloat = float(HBdata)                     #Convert Heart beat String data to Float data.
        TMPfloat = float(TMPdata)                   #Convert Temperature String data to Float data.
        NCint = int(NCdata)                         #Convert Nurse call String data to intiger data.
        
    except:
        print("Invalid entry")                      #If any error on receiving string print
        
    uart_channel.reset_input_buffer()               #Clear receive buffer before read new string from bluetooth     
    uart_channel.flush()

    if (NCint == 1):                                            #If Nurse assistance is needed (NCint is 1)
        GPIO.output(NurseAlert, True)                           #Turn ON LED that indcates Nurse Assistance

    elif (NCint == 0):                                          #If Nurse assistance is not needed (NCint is 0)
        GPIO.output(NurseAlert, False)                          #LED that indcates Nurse Assistance will be OFF

        
    if (HBfloat >= 100 or TMPfloat >= 39.0):                    #For testing purpose Heart Beat is reduced to 100 otherwise it suppose to be 120
        ShortAlert()                                            #Run short Alert

    elif (100 > HBfloat >= 80) or (39.0 > TMPfloat >= 37.5):    #For testing purpose Heart Beat is reduced to 80 otherwise it suppose to be 100
        LongAlert()                                             #Run long Alert

    else:
        HAstate = 0                                             #HAstate is 0
        GPIO.output(buzNlight, False)                           #Buzzer and LED will be off
