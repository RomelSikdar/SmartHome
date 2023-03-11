#include <SPI.h>
#include <PubSubClient.h>
#include <EthernetENC.h>

#define CLIENT_ID "INT01"
#define _host "10.10.1.254"
#define _user "Admin"
#define _pass "iwillhacku"

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
int lastButtonState[] = {
1,1,1,1,1,1,1,1};
int i;
EthernetClient ethClient;
PubSubClient mqttClient;

void(* resetFunc) (void) = 0;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Module Innitialize");
  for (i = 2; i < 10; i++) 
    pinMode(i,INPUT_PULLUP);
  // Check for Ethernet hardware present
  Ethernet.init(17);
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    delay(200);
    resetFunc();
  }
  
  if (Ethernet.linkStatus() == LinkOFF) {
    delay(500);
    if (Ethernet.linkStatus() == LinkOFF) {
      Serial.println("Ethernet cable is not connected.");
      delay(200);
      resetFunc();
    }
  }
  Ethernet.begin(mac,IPAddress(192,168,0,54));
  /*
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Ethernet configuration failed");
    delay(200);
    resetFunc();
  }
*/
  Serial.print("Module IP :- ");
  Serial.println(Ethernet.localIP());

  //Configuring Host
  mqttClient.setClient(ethClient);
  mqttClient.setServer(_host,1883); //for using local broker
  mqttClient.setBufferSize(255);
  while (!mqttClient.connected()) {
    RECONNECT();
  }
}

void loop() {
  if(mqttClient.connected()){
    sendData();
  }else{
    RECONNECT();
  }
  mqttClient.loop();
}

void sendData() {
  char msgBuffer[2];
  for (i = 0; i < 8; i++) {
    if (digitalRead(i+2) != lastButtonState[i]) {
      // if the state has changed, increment the counter
      if (digitalRead(i+2) == 0){
        mqttClient.publish(CLIENT_ID,dtostrf(i, 2, 0, msgBuffer));
        Serial.print("Published button");
        Serial.println(i);
      }
      lastButtonState[i] = digitalRead(i+2);
    }
  }
}

void RECONNECT(){
  Serial.println("Connecting to MQTT...");
  if (mqttClient.connect(CLIENT_ID, _user, _pass )) {
    Serial.println("connected");
  } else {
    Serial.print("failed with state ");
    Serial.print(mqttClient.state());
    delay(2000);
  }
}
