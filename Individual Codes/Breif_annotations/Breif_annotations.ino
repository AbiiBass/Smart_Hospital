
const int smSensor = A2;  // Analog input pin that the soil moisture sensor (smSensor) is connected to

int sensorValue = 0;        // declare sensorValue to store sensor readings later
int NCstate = 0;            //Nurse Calling state officially 0
#define LED 13              //define LED to pin 13

void setup()
{
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(LED 13, OUTPUT); // Declare the LED as an output
}

void loop()
{
  // read the analog sensor value and store in sensorValue.
  sensorValue = analogRead(smSensor);

  // print the results to the Serial Monitor:
  Serial.print("sensor = ");
  Serial.println(sensorValue); // New line after every sensorValue displayed

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
  delay(2);

  if (sensorValue > 100)      //when sensor value is more than 100, it means breif is wet
  {
    NCstate = 1               //NCstate will be 1 to alert Nurses
    Serial.println(NCstate)   //print NCstate value
    digitalWrite(13, HIGH);   //LED ON to alert Nurses

  }

}
