/******Joystick   */
#include<Servo.h>
Servo s2;
/******Joystick^  */

//Arduino Code - RC522 Read RFID Tag UID
#include <SPI.h>            //add SPI
#include <MFRC522.h>        //add MFRC522 file
#include <SoftwareSerial.h> //Blue tooth HC05 as Master interface with software serial 

#define SS_PIN 10           //Pin10 connects to SDA of RFID           
#define RST_PIN 7           //Pin7 connects to Reset of RFID  


//Initilize RFID registers

MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key;
byte PatientID[4];
byte NurseID[4];

/**********************/

//Define Button for Nurse calling
const int buttonPin = 2;
int NC_State = 0;

//Define Moise sensor as detection of urination in the Brief
// These constants won't change. They're used to give names to the pins used:
const int smSensor = A4;    // Analog input pin that the soil moisture sensor (smSensor) is connected to
int MsensorValue = 0;        // declare sensorValue to store sensor readings later

//Setup master HC05 Blue tooth device communicates through So
SoftwareSerial BTSerial(8, 9); //Software UART TX = 8 connects to Tx of HC05 and UART RX = 9 connects to Rx of HC05
//int RxData = 0;
//int Txdata = 0;

//Initilize Heart Beat sensor
#define samp_siz 10         //min4 max 30 this is Heart beat analog sample averging size
#define rise_threshold 6    //min  4 max 10 this is threshold to detect Heart beat analog is raising
#define HB_Avg_siz 20      //min2 max 50 this is to make average on the Heart beat count  
#define TMP_Avg_siz 30      //min2 max 50 this is to make average on the Temperature count 
int sensorPin = A0;
int ThermistorPin = A2;

/******Joystick   */
int p2 = 20;                      // initial position of both servos in degree

int change(int pos, int t)
{
  /******Joystick   */
  pos = pos + t;                // Increment/decrement the Servo angle
  if (pos > 90)                 // maximum anlgle of servo is 90 degree
    pos = 90;
  if (pos < 0)                  // minimum angle of servo is 0 degree
    pos = 0;
  return (pos);                 // return the change of position
  /******Joystick   */
}
/******Joystick   */

void setup()
{
  /******Joystick   */
  s2.attach(4);                  // define pin
  //  pinMode(2, INPUT);              // SW pin status
  //  digitalWrite(2, HIGH);
  /******Joystick   */
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  SPI.begin();        // Init SPI bus
  rfid.PCD_Init();    // Init RC522

  BTSerial.begin(9600);  // initialize blue tooth serial communications at 9600 bps:

  pinMode(buttonPin, INPUT);  //Defing buttonPin=2 as Input pin

}

void printHex(byte *ID, byte *buffer, byte bufferSize)
{
  for (byte i = 0; i < bufferSize; i++)
  {
    ID[i] = buffer[i];
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}



void loop ()
{

  float reads[samp_siz], HB_sample[HB_Avg_siz], TMP_sample[TMP_Avg_siz], sum, HB_sum, TMP_sum;
  long int now, ptr;
  float last, reader, start;
  float first, second, third, before, HB_value, HB_avg;
  bool rising;
  int rise_count, HB_ptr, TMP_ptr;
  int n;
  long int last_beat;

  //Variables for Temperature sensor
  int Vo;
  float R1 = 10000;
  float logR2, R2, T, TMP_avg, TMP_value;
  float c1 = 0.001129148, c2 = 0.000234125, c3 = 0.0000000876741; //steinhart-hart coeficients for thermistor

  for (int i = 0; i < samp_siz; i++)    //initilize Heart beat sensor analog buffer
    reads[i] = 0;

  sum = 0;        //initilize Heart beat sensor analog sum value
  ptr = 0;        //initilize Heart beat sensor analog buffer address pointer

  for (int i = 0; i < HB_Avg_siz; i++)
  {
    HB_sample[i] = 0;     //initilize Heart beat value average buffer
  }
  for (int i = 0; i < TMP_Avg_siz; i++)
  {
    TMP_sample[i] = 0;    //initilize Temperature value average buffer
  }
  HB_avg = 0;             //initilize Heart beat average
  TMP_avg = 0;            //initilize Temperature average
  HB_ptr = 0;             //initilize Heart beat average buffer address pointer
  TMP_ptr = 0;            //initilize Temperature average buffer address pointer
  HB_sum = 0;             //initilize Heart beat sum valuer
  TMP_sum = 0;            //initilize Temperature sum value

  // Initilize RFID bufferes for Patient ID adn Nurse ID
  for (int i = 0; i < 4; i++)
  {
    PatientID[i] = 0;
    NurseID[i] = 0;
  }

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);

  Serial.print(F("RFID Tag UID:"));
  printHex(PatientID, rfid.uid.uidByte, 4);    //printHex(rfid.uid.uidByte, rfid.uid.size);
  Serial.println("");
  //  PatientID[0] = rfid.uid.uidByte[0];            //Buffer 1st byte is PatientID
  rfid.PICC_HaltA(); // Halt PICC

  Serial.println(PatientID[0], HEX);
  int t2 = 0;                     // rate of increment/decrement of angle

  while (PatientID[0] == 0xFA )
  {
    /******Joystick   */

    int b = analogRead(A1);         // reads analog y readings of joystick

    //when joystick is moved away from the center
    if (b <= 250 or b >= 750)
    {
      //Serial.println(b);
      t2 = map(b, 0, 1023, -10, 10);
      p2 = change(p2, t2);          // change the servo's current position
      s2.write(p2);                  // rotate the servo's if the joystick is moved
      delay(90);                      // for Stability
    }


    if (digitalRead(buttonPin) == 0)  // read the digital value of the button and store in buttonPin.
      NC_State = 1;


    MsensorValue = analogRead(smSensor);    // read the analog sensor value and store in sensorValue.
    // wait 2 milliseconds before the next loop for the analog-to-digital
    // converter to settle after the last reading:
    delay(2);
    /********************************************************************************/
    if (MsensorValue > 200)
      NC_State = 1;

    if (NC_State != 0 )
    {

      if ( rfid.PICC_IsNewCardPresent())    // Check if new card present on the sensor/reader.
      {

        if (rfid.PICC_ReadCardSerial())     // Verify if the NUID has been readed
        {
          MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);

          Serial.print(F("RFID Tag UID:"));
          //         printHex(rfid.uid.uidByte, rfid.uid.size);
          printHex(NurseID, rfid.uid.uidByte, 4);
          Serial.println("");
          rfid.PICC_HaltA(); // Halt PICC

          //         NurseID[0] = rfid.uid.uidByte[0];            //Buffer 1st byte is NurseID
          Serial.println(NurseID[0], HEX);
          if (NurseID[0] == 0x73)
            NC_State = 0;
        }
      }
    }


    // calculate an average of the sensor
    // during a 20 ms period (this will eliminate
    // the 50 Hz noise caused by electric light
    n = 0;
    start = millis();
    reader = 0.;
    do
    {
      reader += analogRead (sensorPin);
      n++;
      now = millis();
    }
    while (now < start + 20);
    reader /= n;  // we got an average

    // Add the newest measurement to an array
    // and subtract the oldest measurement from the array
    // to maintain a sum of last measurements
    sum -= reads[ptr];
    sum += reader;
    reads[ptr] = reader;
    last = sum / samp_siz;
    // now last holds the average of the values in the array

    // check for a rising curve (= a heart beat)
    if (last > before)
    {
      rise_count++;
      if (!rising && rise_count > rise_threshold)
      {
        // Ok, we have detected a rising curve, which implies a heartbeat.
        // Record the time since last beat, keep track of the two previous
        // times (first, second, third) to get a weighed average.
        // The rising flag prevents us from detecting the same rise more than once.
        rising = true;
        first = millis() - last_beat;
        last_beat = millis();

        // Calculate the weighed average of heartbeat rate
        // according to the three last beats
        HB_value = 60000. / (0.4 * first + 0.3 * second + 0.3 * third);

        //BTSerial.println(HB_value);    //send the Heart beat value as string with new line feed to Bluetooth HC05
        //         Serial.print("HB :");
        //         Serial.println(HB_value);

        third = second;
        second = first;
        HB_sum -= HB_sample[HB_ptr];  //Subtract the Heart beat count oldest value
        HB_sum += HB_value;           //Add the Heart beat count new value
        HB_sample[HB_ptr] = HB_value; //Replace the Heart beat count oldest value with new value in Circular buffer
        HB_avg = HB_sum / HB_Avg_siz;    //Calculate Heart beat count average
        //BTSerial.print(HB_avg);    //send the Heart beat value as string to Bluetooth HC05

        HB_ptr++;                 //Increment Circular buffer pointer
        HB_ptr %= HB_Avg_siz;        //Circular buffer pointer reset to 0 if exceeds buffer size
      }
    }
    else
    {
      // Ok, the curve is falling
      rising = false;
      rise_count = 0;
    }
    before = last;


    ptr++;
    ptr %= samp_siz;



    // Read Temperature Sensor

    Vo = analogRead(ThermistorPin);
    R2 = R1 * Vo / (1023 - Vo); // calculate resistance on thermistor
    logR2 = log(R2);
    T = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2)); // temperature in Kelvin
    T = T - 293.15;  //273.15; // convert Kelvin to Celcius and remove some offset

    TMP_sum -= TMP_sample[TMP_ptr];
    TMP_sum += T;
    TMP_sample[TMP_ptr] = T;
    TMP_avg = TMP_sum / TMP_Avg_siz;
    TMP_ptr++;                    //increment Circular buffer pointer
    TMP_ptr %= TMP_Avg_siz;           //Circular buffer pointer reset to 0 if exceeds buffer size

    if (TMP_ptr == 0)
    {


      Serial.print(HB_avg, 2);      //send the Heart beat value as string
      Serial.print("&");            //send the & as splitor between Hear beat to Temperature string
      Serial.print(TMP_avg, 2);   //send the Temperature value as string with new line
      Serial.print("&");
      Serial.print(MsensorValue); // print the analog sensor value to the Serial Monitor:
      Serial.print("&");
      Serial.print(NC_State);  // print the digital button value to the Serial Monitor:
      Serial.print("&");

      for (int i = 0; i < 4; i++)
        Serial.print (PatientID[i], HEX);
      Serial.println ("");

      BTSerial.print(HB_avg, 2);    //send the Heart beat value as string to Bluetooth HC05
      BTSerial.print("&");          //send the & as splitor between Hear beat to Temperature string to Bluetooth HC05
      BTSerial.print(TMP_avg, 2); //send the Temperature value as string with new line feed to Bluetooth HC05
      BTSerial.print("&");
      BTSerial.print(NC_State);  // print the digital button value to the Bluetooth HC05:
      BTSerial.print("&");
      for (int i = 0; i < 4; i++)
        BTSerial.print (PatientID[i], HEX);
      BTSerial.println ("");


    }


  }
}
