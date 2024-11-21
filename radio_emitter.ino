/* 
Radio emitter code for the Bumbug.
Made (mostly) by Carlos ★. 

Using radiohead library for protoccoled
serial communitation and messaging.

Used for emitting the data from the
ultrasound sensors to board connected to
computer.
*/

#include <SPI.h>    // Allows conection to peripheral devices
#include <RH_ASK.h> // Actual library used for radio communication
 
// Creates an RH_ASK class
RH_ASK driver;

// Variables requried to cast the to-be-sent message
long distanceLong1;           // Long buffers
long distanceLong2;
double buffDouble = 1000.00;  // Value for integer casting
int len;
int msgSize = 5;
int ascii0 = 48;
char *msg1;
char *msg2;            

// Variables required to calculate distance
double distance1;
double distance2;
double brightness1;
double brightness2;
const double sensorRange = 320;
int sensorDistance;
int echo1 = 7;
int echo2 = 2;
int trigger1 = 7;
int trigger2 = 2;

int led1 = 6;
int led2 = 3;

// Function to meassure distance
long readUltrasonicDistance(int triggerPin, int echoPin)
{
    // Clears trigger pin
    pinMode(triggerPin, OUTPUT);    
    digitalWrite(triggerPin, LOW);  
    delayMicroseconds(2);

    // Triggers a sound wave for 10 microseconds
    digitalWrite(triggerPin, HIGH); 
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);

    // Returns the travel time of the sound wave in microseconds
    pinMode(echoPin, INPUT);
    return pulseIn(echoPin, HIGH); 
}

// Function to cast the message as a char
char *castDistanceAsChar(int msgSize, long distance)
{
    char *msg = (char*) malloc((msgSize + 1) * sizeof(char)); // Allocates memory space for local variable  'msg'
    long valueBuffer = distance; 
    for (int j = msgSize; j >= 0; j--) 
    { 
        msg[j] = (char) ((abs(valueBuffer) % 10) + ascii0);
        /*
        The above stated line works by calculating the distance modulo 10
        (just picking the first digit) and then adding the ascii value for
        0. This is necessary because when casting to the char data type,
        C++ reads what is being casted as an ascii value, to convert to
        the corresponding text.
        */
        valueBuffer /= 10; // Shifts the number by one digit to the right
    }
    return msg;
}
 
void setup()
{
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    driver.init();      // Initializes driver
    Serial.begin(9600); // Debugging only
}
 
void loop()
{
    // Measures the ping time in cm
    distance1 = readUltrasonicDistance(trigger1, echo1) * 0.01724;
    distance2 = readUltrasonicDistance(trigger2, echo2) * 0.01724;
    Serial.println(distance1);
    
    // Turns distance into brightness
    brightness1 = (sensorRange - distance1) * 255 / sensorRange;
    brightness2 = (sensorRange - distance2) * 255 / sensorRange;
    analogWrite(led1, brightness1);
    analogWrite(led2, brightness2);
    
    distanceLong1 = (long) trunc(distance1 * buffDouble); // Casts distances as an integers
    distanceLong2 = (long) trunc(distance2 * buffDouble);

    // Casts distances (integer) as a character lsits
    msg1 = castDistanceAsChar(msgSize, distanceLong1);
    driver.send((uint8_t *)msg1, msgSize + 1); // Sends message 1
    free(msg1);
    driver.waitPacketSent();

    msg2 = castDistanceAsChar(msgSize, distanceLong2);
    driver.send((uint8_t *)msg2, msgSize + 1); // Sends message 2
    free(msg2);
    driver.waitPacketSent();                   // Waits for message 2 to be sent
}
