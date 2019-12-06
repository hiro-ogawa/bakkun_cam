#include <WiFi.h>
#include <PubSubClient.h>
#include <M5Stack.h>
#include <ArduinoJson.h>
#include "AudioFileSourceSD.h"
#include "AudioFileSourceID3.h"
#include "AudioGeneratorMP3.h"
#include "AudioOutputI2S.h"


#define NOTE_DH2 661

// Wi-FiのSSID
char *ssid = "AC9232827A91-2G";
// Wi-Fiのパスワード
char *password = "55401102802042";
// MQTTの接続先のIP
// const char *endpoint = "192.168.39.170";
const char *endpoint = "192.168.3.5";
// MQTTのポート
const int port = 1883;
// デバイスID
char *deviceID = "M5Stack";  // デバイスIDは機器ごとにユニークにします
// メッセージを知らせるトピック
char *pubTopic = "key";
// メッセージを待つトピック
char *subTopic = "/sub/M5Stack";

int keep_alive_time = 100;
char a, b, subMessage;

int yes_val = 0;
int no_val = 0;
int volume = 3;
boolean buton_pressed = false;
String mp3_data;

////////////////////////////////////////////////////////////////////////////////

WiFiClient httpsClient;
PubSubClient mqttClient(httpsClient);

void setup() {
    Serial.begin(115200);

    // Initialize the M5Stack object
    M5.begin();

    // START
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(10, 10);
    M5.Lcd.setTextColor(WHITE);
    M5.Lcd.setTextSize(3);
    M5.Lcd.printf("Take photo?");

    // Start WiFi
    Serial.println("Connecting to ");
    Serial.print(ssid);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    // WiFi Connected
    Serial.println("\nWiFi Connected.");
    M5.Lcd.setCursor(40, 200);
    M5.Lcd.setTextColor(RED);
    M5.Lcd.setTextSize(3);
    M5.Lcd.printf("Yes!!");
    M5.Lcd.setCursor(230, 200);
    M5.Lcd.setTextColor(BLUE);
    M5.Lcd.printf("No!!");

    mqttClient.setServer(endpoint, port);
    mqttClient.setCallback(mqttCallback);
    connectMQTT();
}


void connectMQTT() {
    while (!mqttClient.connected()) {
        if (mqttClient.connect(deviceID)) {
            Serial.println("Connected.");
            int qos = 0;
            mqttClient.subscribe(subTopic, qos);
            Serial.println("Subscribed.");
        } else {
            Serial.print("Failed. Error state=");
            Serial.print(mqttClient.state());
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}


char pubMessage[128];

AudioGeneratorMP3 *mp3;
AudioFileSourceSD *file_m;
AudioOutputI2S *out_m;
AudioFileSourceID3 *id3;

// 音声を再生する
void play_audio(String data){
    if (mp3_data != ""){
        Serial.println(mp3_data);
//         file_m = new AudioFileSourceSD("¥""+/+mp3_data+""¥");
        file_m = new AudioFileSourceSD("/assets/b7.mp3");
        id3 = new AudioFileSourceID3(file_m);
        out_m = new AudioOutputI2S(0,1);
        out_m->SetOutputModeMono(true);
        out_m->SetGain(0.3);
        mp3 = new AudioGeneratorMP3();
        mp3->begin(id3, out_m);
        while(mp3->isRunning()){
         if (!mp3->loop()) mp3->stop();
         }
    }
}

// subscribeする
void mqttCallback (char* topic, byte* payload, unsigned int length) {
    String str = "";
    Serial.print("Received. topic=");
    Serial.println(topic);
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
        str += (char)payload[i];
    }
    mp3_data = str;
    play_audio(mp3_data);
    Serial.print("\n");
}

void mqttLoop() {
    if (!mqttClient.connected()) {
        connectMQTT();
    }
    mqttClient.loop();
}

void loop() {
    buton_pressed = false;
    mqttLoop();
    M5.update();

    if (M5.BtnA.wasReleased()){
        sprintf(pubMessage, "y");
        buton_pressed = true;
    }
    else if (M5.BtnC.wasReleased()){
        sprintf(pubMessage, "n");
        buton_pressed = true;
    }
    if (buton_pressed){
        mqttClient.publish(pubTopic, pubMessage);
        Serial.println(pubMessage);
    }
    delay(100);
}