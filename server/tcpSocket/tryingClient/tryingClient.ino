#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Servo.h> 
const uint16_t port = 65432;
const char *host = "192.168.0.187";
int servoPin = 16; 
int servoCounter=0;
int servoDirection=0;
Adafruit_MPU6050 mpu;
Servo Servo1; 
WiFiClient client;
void setup()
{
       Servo1.attach(servoPin);  
    Serial.begin(115200);
    Serial.println("Connecting...\n");
    WiFi.mode(WIFI_STA);
    WiFi.begin("TP-LINK_AZI_3_2G", "Suzi12345612!"); // change it to your ussid and password
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    client.connect(host, port);
    Serial.println("Connected to server successful!");
    if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
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
     servoCounter+=8;
   } 
   else{
     servoCounter-=8;
   } 
//   delay(6); 

} 
void loop()
{
  doServo();
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  String accTitle=" Acceleration ";
  String rotTitle=" Rotation ";
  String tempTitle=" Temperature ";
  String space=" ";
  String accMsg = accTitle + a.acceleration.x+space+a.acceleration.y+space+a.acceleration.z;
  String rotMsg = rotTitle + space+g.gyro.x+space+g.gyro.y+space+g.gyro.z;
  String tempMsg = tempTitle + temp.temperature;

  client.print(accMsg+rotMsg+tempMsg); 
  delay(50); 
//    while (client.available() > 0)
//    {
//        char c = client.read();
//        Serial.write(c);
//    }
    Serial.print('\n');
//    client.stop();
//    delay(5000);
}
