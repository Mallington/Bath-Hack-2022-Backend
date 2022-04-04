#include <Arduino.h>

#define A 12
#define B 11
#define C 10
#define D 9
 
#define NUMBER_OF_STEPS_PER_REV 512

#define RELAY_FIRE 7

#define HALT 0
#define CLOCKWISE 1
#define ANTICLOCKWISE 2
int motorState = HALT;

void write(int a,int b,int c,int d){
digitalWrite(A,a);
digitalWrite(B,b);
digitalWrite(C,c);
digitalWrite(D,d);
}

void antiStep(int delayAmount){
write(1,0,0,0);
delay(delayAmount);
write(1,1,0,0);
delay(delayAmount);
write(0,1,0,0);
delay(delayAmount);
write(0,1,1,0);
delay(delayAmount);
write(0,0,1,0);
delay(delayAmount);
write(0,0,1,1);
delay(delayAmount);
write(0,0,0,1);
delay(delayAmount);
write(1,0,0,1);
delay(delayAmount);
}

void clockStep(int delayAmount){
write(1,0,0,1);
delay(delayAmount);
write(0,0,0,1);
delay(delayAmount);
write(0,0,1,1);
delay(delayAmount);
write(0,0,1,0);
delay(delayAmount);
write(0,1,1,0);
delay(delayAmount);
write(0,1,0,0);
delay(delayAmount);
write(1,1,0,0);
delay(delayAmount);
write(1,0,0,0);
delay(delayAmount);
}

void setup(){
pinMode(A,OUTPUT);
pinMode(B,OUTPUT);
pinMode(C,OUTPUT);
pinMode(D,OUTPUT);
pinMode(RELAY_FIRE, OUTPUT);
Serial.begin(9600);

}

void loop(){

  if(Serial.available()){
    char readChar = Serial.read();
    switch (readChar)
    {
    case 'f':
      digitalWrite(RELAY_FIRE, HIGH);
      break;
    
    case 'c':
      digitalWrite(RELAY_FIRE, LOW);
      break;
    case 'l':
      motorState = ANTICLOCKWISE;
      break;
    case 'r':
      motorState= CLOCKWISE;
      break;
    case 'h':
      motorState = HALT;
      break;
    
    case 'e':
      motorState = HALT;
      break;
    
    default:
      break;
    }
  }

  switch (motorState)
  {

  case CLOCKWISE:
    clockStep(5);
    break;
  case ANTICLOCKWISE:
    antiStep(5);
    break;
  }


} 


