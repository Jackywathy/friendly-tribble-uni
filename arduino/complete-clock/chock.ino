#include <SevSeg.h>

#include <RTClib.h>
#include <Wire.h>


#define RTC_NOT_FOUND 25


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



#define INTERRUPT_HOUR 10
#define INTERUPT_MINUTE 11

RTC_DS3231 rtc;

SevSeg myDisplay;

unsigned long timer;

void setup(){
  Serial.begin(9600);
  Serial.println("setup()");
  
  // setup RTC  
  if (!rtc.begin()){
    errorCode(RTC_NOT_FOUND);
  }
  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  char timeString[5];
  
  // setup CLOCK
  int displayType = COMMON_CATHODE;
  int numberOfDigits = 4;
  
  myDisplay.Begin(displayType, numberOfDigits, digit1, digit2, digit3, digit4, segA, segB, segC, segD, segE, segF, segG, segDP);
  myDisplay.SetBrightness(80);
  
  timer = millis();
  // SET interrupts
}



void loop(){
  //DateTime now = rtc.now();
  
  char buffer[10];
  //int hour = now.hour();
  //int minute = now.minute();
  int hou
  sprintf(buffer, "%4d", hour);
  myDisplay.DisplayString(buffer, 0);
  
  if (millis() - timer >= 10)
  {
    timer = millis();
    Serial.println(buffer);
  }

}

void errorCode(int code){
  char printCode[5];
  sprintf(printCode , "%4d", code);
  while(1){
    myDisplay.DisplayString(printCode, 0);
  }
}
