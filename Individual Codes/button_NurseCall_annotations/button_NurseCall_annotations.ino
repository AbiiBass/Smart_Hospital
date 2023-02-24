//constants
const int buttonPin = 2;      // the number of the pushbutton pin
#define LED 13                //define LED to pin 13
// variables
int buttonState = 0;         // variable for reading the pushbutton status
int NCstate = 0;             //initialize Nurse Calling state as 0
void setup() 
{
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT); //Declare buttonPin as input
  pinMode(LED 13, OUTPUT); //Declare the LED as an output
}

void loop() 
{
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH)    //when button pressed, it means patient needs assistance 
  {
    NCstate = 1;              //NCstate will be 1
    Serial.println(NCstate);  //print NCstate value
    digitalWrite(13, HIGH);   //LED ON to alert Nurses
  }
}
