// #include <WiFi.h>

// // WiFi credentials
// const char* ssid = "raspWIFI";         // Replace with your SSID
// const char* password = "raspwifi"; // Replace with your password

// // Server details
// const char* host = "10.42.0.229";    // Replace with the server IP address or domain name
// const uint16_t port = 6420;            // Replace with the server port
// const uint16_t port1 = 6421;
// // ADC Pin
// const int adcPin = 34; // GPIO34 is an ADC1 channel

// WiFisender sender;
// WiFisender sender1;

// void setup() {
//   // 
//   delay(10);

//   // // Connect to WiFi
//   // 
//   // 
//   // 
  
//   WiFi.begin(ssid, password);

//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     // 
//   }

//   // 
//   // 
//   // 
//   // 
//   if (!sender.connect(host, port)) {
//     // 
//     delay(1000);
//   }
//   if (!sender1.connect(host, port1)) {
//     // 
//     delay(1000);
//   }
// }

// void loop() {
//   // Read ADC value
//   int adcValue = analogRead(adcPin);
  
//   // Convert ADC value to voltage (assuming 12-bit ADC and 3.3V reference voltage)
//   float voltage = adcValue * (3.3 / 4095.0);
  
//   // Create a TCP connection to the server

//   if (!sender.connected()) {
//     // 
//     delay(1000);
//     return;
//   }
  
//   // Send the ADC value (or voltage) to the server
//   sender.print(String(adcValue) + "\n");
  
//   // Wait for a bit before sending the next reading
//   //delay(1000);
// }

// void loop1() {
  
//   // Create a TCP connection to the server

//   if (!sender1.connected()) {
//     // 
//     delay(1000);
//     return;
//   }
  
//   // Send the ADC value (or voltage) to the server
//   sender1.print(String(24) + "\n");
  
//   // Wait for a bit before sending the next reading
//   //delay(1000);
// }
#include <WiFi.h>

// WiFi credentials
const char* ssid = "raspWIFI";         // Replace with your SSID
const char* password = "raspwifi"; // Replace with your password

// Server details
const char* host = "10.42.0.229";    // Replace with the server IP address or domain name
const uint16_t port = 6420;            // Replace with the server port
const uint16_t port1 = 6421;
WiFiClient sender;
//WiFiClient receiver;

// ADC Pin
const int adcPin = 34; // GPIO34 is an ADC1 channel
const int dacPin = 25;

// Function prototypes
void receiveTask(void *pvParameters);
void sendTask(void *pvParameters);

void setup() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  
  }
  
  if (!sender.connect(host, port)) {
    delay(1000);
  }
  // if (!receiver.connect(host, port1)) {
  //   delay(1000);
  // }
  delay(10);

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
  /*xTaskCreatePinnedToCore(
    receiveTask,         // Task function
    "receiveTask",       // Name of the task (for debugging)
    4096,             // Stack size (bytes)
    NULL,             // Task input parameter
    1,                // Priority of the task
    NULL,             // Task handle
    1
  );*/
}

void loop() {
  // Do nothing in the loop
}

void sendTask(void *pvParameters) {
  int16_t adcValue = 0;
  while (true) {
    // Read ADC value
    adcValue = analogRead(adcPin);
    if(sender.connected()){
      sender.write(adcValue>>4);
    }
  }
}

// void receiveTask(void *pvParameters) {
//   uint8_t buffer;
//   while (true) {
//     if(receiver.connected()){
//       receiver.readBytes(&buffer, sizeof(uint8_t));
//       dacWrite(dacPin, buffer);
//     }
    
//     // if (buffer[0] == '1')
//     //   digitalWrite(12, HIGH);
//     // if (buffer[0] == '0')
//     //   digitalWrite(12, LOW);
//   }
// }
