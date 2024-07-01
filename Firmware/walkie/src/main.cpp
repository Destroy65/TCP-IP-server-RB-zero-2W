#include <WiFi.h>

// WiFi credentials
const char* ssid = "raspWIFI";        
const char* password = "raspwifi"; 

// Server details
const char* host = "10.42.0.229";   
const uint16_t sPort = 6420;            
const uint16_t rPort = 6421;
WiFiClient sender;
WiFiServer receiver(rPort);

// ADC Pin
const int adcPin = 34; 
const int dacPin = 25;

// Function prototypes
void receiveTask(void *pvParameters);
void sendTask(void *pvParameters);

void setup() {
  // Serial.begin(9600);
  // Serial.print("Connecting to ");
  // Serial.println(ssid);

  // WiFi.begin(ssid, password);

  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(500);
  //   Serial.print(".");
  // }
  
  // Serial.println("");
  // Serial.println("WiFi connected");
  // Serial.println("IP address: ");
  // Serial.println(WiFi.localIP());

  // Serial.println("Connection established to:");
  // Serial.println("10.42.0.1:6420");
  // Serial.println("Connection to port 6421 accepted from:");
  // Serial.println("10.42.0.1");
  // while (!sender.connect(host, sPort)) {
  //   delay(1000);
  // }

  // receiver.begin();
  // delay(10);

  // Create the ADC task
  xTaskCreatePinnedToCore(
    sendTask,          // Task function
    "sendTask",        // Name of the task (for debugging)
    4096,             // Stack size (bytes)
    NULL,             // Task input parameter
    1,                // Priority of the task
    NULL,              // Task handle
    0
  );

  // Create the WiFi task
  // xTaskCreatePinnedToCore(
  //   receiveTask,         // Task function
  //   "receiveTask",       // Name of the task (for debugging)
  //   4096,             // Stack size (bytes)
  //   NULL,             // Task input parameter
  //   1,                // Priority of the task
  //   NULL,             // Task handle
  //   1
  // );
}

void loop() {
  // Do nothing in the loop
}

void sendTask(void *pvParameters) {
  int16_t adcValue = 0;
  while (true) {
    // Read ADC value
    adcValue = analogRead(adcPin);
    // if(sender.connected()){
    //   sender.write((adcValue>>6)&0xFF);
    // }
    dacWrite(25, (adcValue>>6)&0xFF);
    delayMicroseconds(125);
  }
}

void receiveTask(void *pvParameters) {
  while (true)
  {
    WiFiClient client = receiver.available();
    if (client){
      uint8_t buffer;
      while (client.connected()) {
        if(client.available()){
          client.readBytes(&buffer, sizeof(uint8_t));
          dacWrite(dacPin, buffer);
        }
      }
      client.stop();
    }
  }
}
