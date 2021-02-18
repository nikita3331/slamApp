#include <Arduino.h>
#include <Wire.h>
#include <Servo.h> 
#include <SoftwareSerial.h>
int servoPin = 49; 
int servoCounter=0;
int servoDirection=0;
Servo Servo1; 
SoftwareSerial ArduinoUno(51,53);

void setup()
{
  pinMode(servoPin, OUTPUT);    // sets the digital pin 13 as output

       Servo1.attach(servoPin);  
   ArduinoUno.begin(115200);

  }

int pos = 0;    // variable to store the servo position
const byte numPins = 7;
byte pins[] = {2,3,4,5,6,7,8};
void printValues(){
    for (byte i=0; i<numPins; i++) {
      byte state = bitRead(pos, i);
      digitalWrite(pins[i], HIGH);
    }
    ArduinoUno.println(pos);
}
void doServo(){

  for (pos = 0; pos <= 180; pos += 2) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    Servo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    printValues();
  }
  for (pos = 180; pos >= 0; pos -= 2) { // goes from 180 degrees to 0 degrees
    Servo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    printValues();
  }

} 
void loop()
{
  doServo();

}
