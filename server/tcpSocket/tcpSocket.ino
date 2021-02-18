#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h> 
const uint16_t port = 65432;
const char *host = "192.168.0.187";
SoftwareSerial NodeMCU(D6,D5);

int servoPin = 16; 
int servoCounter=0;
int servoDirection=0;
Adafruit_MPU6050 mpu;
const int trigPin = 2;
const int echoPin = 0;
// defines variables
long duration;
float distance=0;

Servo Servo1; 
WiFiClient client;
void setup()
{
     NodeMCU.begin(115200);
    Serial.begin(9600);
       Servo1.attach(servoPin);  
    WiFi.mode(WIFI_STA);
    WiFi.begin("TP-LINK_AZI_3_2G", "Suzi12345612!"); // change it to your ussid and password
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }
    client.connect(host, port);
    if (!mpu.begin()) {
    while (1) {
      delay(10);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
}
void doServo(){
    Servo1.write(servoCounter);
   if(servoCounter>180){
     servoDirection=1;
   }
   if(servoCounter<0){
     servoDirection=0;
   }
  if(servoDirection==0){
     servoCounter+=1;
   } 
   else{
     servoCounter-=1;
   } 
   delay(6); 
} 
void getDistance(){
  digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance= duration*0.034/2;
Serial.println(distance);
}

void loop()
{
//  doServo();
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  String accTitle=" Acceleration ";
  String rotTitle=" Rotation ";
  String tempTitle=" Temperature ";
  String space=" ";
  String accMsg = a.acceleration.x+space+a.acceleration.y+space+a.acceleration.z;
  String rotMsg = space+g.gyro.x+space+g.gyro.y+space+g.gyro.z;
  String tempMsg = space+temp.temperature;


String content = "";
char character;

  while(NodeMCU.available()) {
      character = NodeMCU.read();
      content.concat(character);
  }


String ending=":"
  client.print(accMsg+rotMsg+tempMsg+space+content+space+distance+ending);  
    while (client.available() > 0)
    {
        char c = client.read();
//        Serial.write(c);
    }
    delay(10);
//    client.stop();
//    ==delay(5000);
}
