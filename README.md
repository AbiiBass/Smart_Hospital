# Smart_Hospital
This project involves communication between Raspberry Pi and Arduino Uno. Communication is done through bluetooth. Besides communicating with Raspberry Pi, Arduino also communicated with Alexa through Wi-Fi switch. This is a student project done in the time scope mid December 2021 to January 2022. <br /> 
Video Description of the Project
https://youtu.be/XvT4zGkShr4

| Devices Used |   | Componenets |   | Programming Languags |
|--------------|---|-------------|---|----------------------|
| Raspberry Pi |   | RFID Sensor |   | Python (Raspberry Pi)|
| Arduino Uno  |   | Heart Rate Sensor | | Arduino C |
| | | Temperature Sensor | | |
| | | Moisture Sensor | | |
| | | Joystick and Switch | | |
| | | Wi-Fi Switch | | |
| | | HC05 Device | | |
| | | Servo Motor | | |
| | | Buzzer | | |
| | | LEDs | | |
| | | Motion Sensor | | |
| | | Ultrasonic Sensor | | |
| | | Speaker + Microphone (ISD1820) | | |
| | | DHT11 | | |
| | | DC Motor | | |

<br />
<br />
<br />


| Arduino |
|---------|
| Most components related to patient is connected to the Arduino. There is one Arduino attached to each patient bed. Datas such as the bed ID, and all sensor data is sent to raspberry pi wirelessly through bluetooth communication. |
| sensors attaced to Arduino: Heart Rate sensor, Temperature Sensor, Moisture Sensor, Joystick, Servo Motor, **__Wi-Fi Switch__** and HC05 Bluetooth device|
| Wifi Switch |
| This is for patients to have control over the room lights and also to call for help. Besides click on the help call button, patients can also call for help through Alexa  |

<br />
<br />
<br />

| Raspberry Pi |
|--------------|
| Connected components are for operating basic features in the hospital. The Raspberry Pi aslo receives information from Arduino and sends the data to ThingSpeak. This data can be viewed by the nurses either through a mobile app created using MIT App Inventor or computer. Data displayed will patients pulse rate and temperature. On a case where a patient's pulsrate or temperature increases to unhealthy level, there will be an alarm to notify all staff for quick help |




