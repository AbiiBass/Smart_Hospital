//Arduino Code - RC522 Read RFID Tag UID
 
#include <SPI.h>            //add SPI
#include <MFRC522.h>        //add MFRC522 file
 
#define SS_PIN 10           //Pin10 connects to SDA of RFID        
#define RST_PIN 7           //Pin7 connects to Reset of RFID  
 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
 
MFRC522::MIFARE_Key key;

 
void setup() { 
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init RC522 
}
 
void loop() 
{

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
 
  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;
 
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
 
  Serial.print(F("RFID Tag UID:"));
  printHex(rfid.uid.uidByte, rfid.uid.size);
  
  Serial.println("");
 
  rfid.PICC_HaltA(); // Halt PICC
  


}
 
//Routine to dump a byte array as hex values to Serial. 
void printHex(byte *buffer, byte bufferSize) 
{
  for (byte i = 0; i < bufferSize; i++) 
  {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");              //print Tag ID in Hexadecimal format
    Serial.print(buffer[i], HEX);
  }
} 
