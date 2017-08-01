#include <RTClib.h>
#include <Wire.h>

RTC_DS3231 rtc;

#include "SevSeg.h"

#define digit1 12
#define digit2 9
#define digit3 8
#define digit4 6

#define segA 11
#define segB 7
#define segC 4
#define segD 2
#define segE 1
#define segF 10
#define segG 5
#define segDP 3


//Create an instance of the object.
SevSeg myDisplay;

//Create global variables
unsigned long timer;

int brightness = 80;


void setup()
{
  //Serial.begin(9600);
  int displayType = COMMON_ANODE; //Your display is either common cathode or common anode
  //This pinout is for a regular display
  //Declare what pins are connected to the digits


  int numberOfDigits = 4; //Do you have a 1, 2 or 4 digit display?

  myDisplay.Begin(displayType, numberOfDigits, digit1, digit2, digit3, digit4, segA, segB, segC, segD, segE, segF, segG, segDP);

  myDisplay.SetBrightness(brightness); //Set the myDispldisplay to 100% brightness level


  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
  pinMode(segDP, OUTPUT);
  timer = millis();
  
}


void loop()
{
  DateTime now = rtc.now();
  //Example ways of displaying a decimal number
  int hour = now.hour();
  while(hour >=12){
    hour -= 12;
  }
  int minute = now.minute();
  while (minute >= 60){
    minute -= 60;
  }
  char tempString[10]; //Used for sprintf
  sprintf(tempString, "%02d", hour); //Convert deciSecond into a string that ibrighright adjusted
  sprintf(tempString+2, "%02d", minute);

  //Produce an output on the display
  myDisplay.DisplayString(tempString, 3); //(numberToDisplay, decimal point location)

  //Other examples
  //myDisplay.DisplayString(tempString, 0); //Display string, no decimal point
  //myDisplay.DisplayString("-23b", 3); //Display string, decimal point in third position

  //Check if 10ms has elapsedsi
  unsigned long timestamp = millis();
  if (timestamp - timer >= 1000){
    timer = millis();
  } 
  if (timestamp - timer <= 450){
    digitalWrite(segDP, HIGH);
    digitalWrite(digit3, HIGH);
    digitalWrite(digit4, HIGH);
    delayMicroseconds(myDisplay.brightnessDelay+1);
    digitalWrite(segDP, LOW);
    digitalWrite(digit3, LOW);
    digitalWrite(digit4, LOW);
    delayMicroseconds(2000 - myDisplay.brightnessDelay + 1);

  }
  delay(5);
}


