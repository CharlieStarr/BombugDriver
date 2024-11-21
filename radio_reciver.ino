/* 
Radio reciver code for the Bombug.
Made (mostly) by Carlos ★. 

Using radiohead library for protoccoled
serial communitation and messaging.

Used for recieving data from the ultrasound
sensors board.
*/

#include <SPI.h>    // Allows conection to peripheral devices
#include <RH_ASK.h> // Actual library used for radio communication

RH_ASK driver; // Creates an RH_ASK class

const byte msgSize = 6;
 
void setup()
{
    driver.init();      // Initializes driver
    Serial.begin(9600); // Debugging only??
}
 
void loop()
{
    uint8_t msg[msgSize];           // Creates message with expected lenght
    uint8_t msgLen = sizeof(msg); 
    if (driver.recv((uint8_t *)msg, &msgLen)) // Recieves message
    {
         // Prints recieved message to the serial monitor
         Serial.println((char *)msg);         
    }
}
