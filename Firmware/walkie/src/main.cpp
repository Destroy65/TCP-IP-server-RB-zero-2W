#include <WiFi.h>

#define BUFF_SIZE 100
// WiFi credentials
const char* ssid = "raspWIFI";        
const char* password = "raspwifi"; 

// Server details
const char* host = "10.42.0.1";   
const uint16_t sPort = 6420;            
const uint16_t rPort = 6421;
WiFiClient sock;
//WiFiServer receiver(rPort);

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

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // Serial.println("");
  // Serial.println("WiFi connected");
  // Serial.println("IP address: ");
  // Serial.println(WiFi.localIP());

  // Serial.println("Connection established to:");
  // Serial.println("10.42.0.1:6420");
  // Serial.println("Connection to port 6421 accepted from:");
  // Serial.println("10.42.0.1");
  // receiver.begin();
  // delay(10);
  
  while (!sock.connect(host, sPort)) {
    delay(1000);
  }

  

  // Create the ADC task
  xTaskCreatePinnedToCore(
    sendTask,          // Task function
    "sendTask",        // Name of the task (for debugging)
    8192,             // Stack size (bytes)
    NULL,             // Task input parameter
    1,                // Priority of the task
    NULL,              // Task handle
    0
  );

  // Create the WiFi task
  xTaskCreatePinnedToCore(
    receiveTask,         // Task function
    "receiveTask",       // Name of the task (for debugging)
    8192,             // Stack size (bytes)
    NULL,             // Task input parameter
    1,                // Priority of the task
    NULL,             // Task handle
    1
  );
}

void loop() {
  // Do nothing in the loop
}

void sendTask(void *pvParameters) {
  int16_t adcValue = 0;
  uint8_t buff[BUFF_SIZE];
  while (true) {
    // Read ADC value
    for(int i = 0; i < BUFF_SIZE; i++){
      adcValue = analogRead(adcPin);
      buff[i] = (adcValue>>4)&0xFF;
      delayMicroseconds(125);
    }
    if(sock.connected()){
      sock.write(buff, BUFF_SIZE);
    }
    //dacWrite(25, (adcValue>>6)&0xFF);
    
  }
}

void receiveTask(void *pvParameters) {
  int16_t dacValue = 0;
  uint8_t buff[BUFF_SIZE];
  while (true)
  {
    if(sock.connected() && sock.available()){
        sock.readBytes(buff, BUFF_SIZE); 
      for (int i = 0; i < BUFF_SIZE; i++){
        dacValue = buff[i];
        dacWrite(dacPin, dacValue);
        delayMicroseconds(125);
      }
    }
  }
}
