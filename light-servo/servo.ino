#include <IRremote.h>
#include <IRremoteInt.h>


#include <Servo.h>
#define PIN_TURNOFF A0
#define PIN_TURNON A1
#define TIME_DELAY 1000
#define REMOTE_UP 16736925
#define REMOTE_DOWN 16754775

void turnOffSwitch(void);
void turnOnSwitch(void);

Servo turnOff, turnOn;
IRrecv reciever(11);

void setup() {
  reciever.enableIRIn();
  Serial.begin(9600);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
}

void loop() {
  decode_results results;
  if (reciever.decode(&results)){
    switch(results.value){
      case (REMOTE_UP):
      Serial.println("UP");
        turnOnSwitch();
        
        break;
      
      case (REMOTE_DOWN):
      Serial.println("DOWN");
        turnOffSwitch();
        
        break;
      default:
        Serial.println(results.value);
        break;
      
    }
    reciever.resume();
  }
  //turnOffSwitch();
  
}

void turnOffSwitch(){
  turnOff.attach(PIN_TURNOFF);
  turnOff.write(100);
  delay(TIME_DELAY);
  turnOff.write(10);
  delay(TIME_DELAY);  
  turnOff.detach();
}
void turnOnSwitch(){
  turnOn.attach(PIN_TURNON);
  turnOn.write(163);
  delay(TIME_DELAY);
  turnOn.write(80);
  delay(TIME_DELAY);
  turnOn.detach();
}
