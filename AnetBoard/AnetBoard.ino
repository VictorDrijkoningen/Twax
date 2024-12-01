#include <ArduinoJson.h>
#define minlooptime 50
#define senddatatimeout 500
#define recvdatatimeout 100

#include "AccelStepper.h"
#define EnablePin 14
#define LdrivePin 15
#define LdriveDirPin 21
#define RdrivePin 22
#define RdriveDirPin 23
AccelStepper ldrive = AccelStepper(1, 15, 21);
AccelStepper rdrive = AccelStepper(1, 22, 23);


JsonDocument send;
int maxdatalength = 5;
int readerror = 0;

long lastsend = 0;
long lastrecv = 0;

int lspeed = 0;
int rspeed = 0;

void setup() {
  send["readerror"] = 0;
  pinMode(EnablePin, OUTPUT);

  rdrive.setMaxSpeed(10000);
  ldrive.setMaxSpeed(10000);

  Serial.begin(115200);
  Serial.println("Start");
}

void send_data(){
  if (millis()-lastsend < senddatatimeout){return;}
  lastsend = millis();

  send["anetserialavailable"] = Serial.available();
  send["readerror"] = readerror;

  serializeJson(send, Serial);
  Serial.println("");
}

void recv_data(){
  if (millis()-lastrecv < recvdatatimeout){return;}
  lastrecv = millis();


  if (Serial.available() > maxdatalength){
    if (Serial.find("a")){
      lspeed = Serial.read();
      lspeed = lspeed - 100;
    } else {
      readerror += 1;
    }

    if (Serial.find("b")){
      rspeed = Serial.read();
      rspeed = rspeed - 100;
    } else {
      readerror += 1;
    }

    on_recv();
  }
}


void on_recv(){
  send["lspeed"] = lspeed;
  send["rspeed"] = rspeed;

  ldrive.setSpeed(-lspeed*100);
  rdrive.setSpeed(-rspeed*100);
}


void loop() {
  send_data();
  recv_data();
  

  ldrive.runSpeed();
  rdrive.runSpeed();

  
}
