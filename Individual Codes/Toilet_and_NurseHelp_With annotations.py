#The toilet with help buttons as well
import RPi.GPIO as GPIO                                         #import Raspberry Pi GPIO module as GPIO
import time                                                     #import time
GPIO.setwarnings(False)                                         #disable warnings
GPIO.setmode(GPIO.BCM)                                          #set Broadcom SOC channel


###Inputs###
MS = 26                                                         #insert MS(Motion Sensor) at GPIO pin 26
GPIO.setup (MS, GPIO.IN)                                        #set GPIO pin 26 as input

ToiletButton = 12                                               #insert help button in Toilet (ToiletButton) at GPIO pin 12
ShowerButton = 20                                               #insert help button in Shower (ShowerButton) at GPIO pin 20
GPIO.setup(ToiletButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)   #set GPIO pin 12 as input
GPIO.setup(ShowerButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)   #set GPIO pin 20 as input

CancelTbutton = 16                                              #insert cancel help button (CancelTbutton) in Toilet at GPIO pin 16
CancelSbutton = 21                                              #insert cancel help button (CancelSbutton) in Shower at GPIO pin 21
GPIO.setup(CancelTbutton, GPIO.IN, pull_up_down = GPIO.PUD_UP)  #set GPIO pin 16 as input
GPIO.setup(CancelSbutton, GPIO.IN, pull_up_down = GPIO.PUD_UP)  #set GPIO pin 21 as input


FanMotorA = 23                                                  #insert fanA motor (FanMotorA) in Toilet at GPIO pin 23                         
fanmotorB = 24                                                  #insert fanB motor (FanMotorB) in Toilet at GPIO pin 24
GPIO.setup(FanMotorA, GPIO.OUT)                                 #set GPIO pin 23 as output
GPIO.setup(fanmotorB, GPIO.OUT)                                 #set GPIO pin 24 as output

HelpLights = 13                                                 #insert Help Lights (HelpLights) at GPIO pin 13
GPIO.setup(HelpLights, GPIO.OUT)                                #set GPIO pin 13 as output

help_state = 0                                                  #help_state is originally 0
no_help = 0                                                     #no_help is orginally 0


def occupied():                                                 #Define "occupied" as...
    GPIO.output(FanMotorA, True)                                #Motor On#
    GPIO.output(fanmotorB, False)                               ##########
    
def empty():                                                    #Define "empty" as...
    GPIO.output(FanMotorA, False)                               #Motor Off#
    GPIO.output(fanmotorB, False)                               ###########

def HELP():                                                     #Define "Help"
    GPIO.output(HelpLights, True)                               #HelpLights turn ON
    help_state = 1                                              #help_state will be 1

def no_HELP():                                                  #Define "no_HELP"
    GPIO.output(HelpLights, False)                              #HelpLights turn OFF  
    no_help = 1                                                 #no_help state will be 1
    help_state = 0                                              #help_state will be 0

    
SI = False                                                      #SI short for "Someone Inside" will be originally False

no_HELP()                                                       #run "no_HELP" a first

while True:
    Msensor = GPIO.input(MS)                                    #define Msensor as GPIO.input(MS)

    Help_at_Toilet = GPIO.input(ToiletButton)                   #define Help_at_Toilet as GPIO.input(ToiletButton)
    Help_at_Shower = GPIO.input(ShowerButton)                   #define Help_at_shower as GPIO.input(ShowerButton)
    CancelToilet = GPIO.input(CancelTbutton)                    #define CancelToilet as GPIO.input(CancelTbutton)
    CancelShower = GPIO.input(CancelSbutton)                    #define CancelShower as GPIO.input(cancelSbutton

    if Msensor == True:                                         #When motion is detected
        occupied()                                              #run "occuopied" function
        SI = True                                               #SI will be True
    
    elif SI == True and Msensor == False:                       #After SI is True and no motion is detected
        time.sleep(5)                                           #hold for 5 seconds to confirm no motion is detected (real time value 10 minutes)
                                                                #   if motion is detected in between 5 seconds, won't continue and time will restart
        empty()                                                 #run "empty" function 
        SI = False                                              #SI will be False (back to original)
                                                                #________________________Later it continues as a loop
        
        
                                                                                        #####################################                                                                                   
    if ((Help_at_Toilet == False) or (Help_at_Shower == False)):                        #                                   #
        HELP()                                                                          #  When any help button is pressed  #
                                                                                        #       run "HELP" function         #
    elif (help_state == 1 and ((Help_at_Toilet == True) or (Help_at_Shower == True))):  #                                   #
        HELP()                                                                          #####################################

                                                                                        ########################################
    elif ((CancelToilet == False) or (CancelShower == False)):                          #                                      #
        no_HELP()                                                                       #  When cancel help button is pressed  #
                                                                                        #       run "no_HELP" function         #        
    elif (no_help == 1 and ((CancelToilet == True) or (CancelShower == False))):        #                                      #
        no_HELP()                                                                       ########################################                                                                       


