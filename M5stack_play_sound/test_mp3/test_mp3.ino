
#pragma mark - Depend ESP8266Audio and ESP8266_Spiram libraries
/*
cd ~/Arduino/libraries
git clone https://github.com/earlephilhower/ESP8266Audio
git clone https://github.com/Gianbacchio/ESP8266_Spiram
*/


#include <M5Stack.h>
#include <WiFi.h>
#include "AudioFileSourceSD.h"
#include "AudioFileSourceID3.h"
#include "AudioGeneratorMP3.h"
#include "AudioOutputI2S.h"


AudioGeneratorMP3 *mp3;
AudioFileSourceSD *file_m;
AudioOutputI2S *out_m;
AudioFileSourceID3 *id3;

bool button_clicked = false;

void setup() {
  M5.begin();
  delay(500);
}

void loop(){
  M5.update();

  if(M5.BtnA.wasPressed()){
    //MP3の場合
    //毎回 new AudioFileSourceSD作りなおさなきゃいけないらしい
    button_clicked = true;
    file_m = new AudioFileSourceSD("/test1.mp3");
    }
  if(M5.BtnC.wasPressed()){
    button_clicked = true;
    file_m = new AudioFileSourceSD("/test2.mp3");

  }
  if(button_clicked){
    id3 = new AudioFileSourceID3(file_m);
    out_m = new AudioOutputI2S(0,1);
    out_m->SetOutputModeMono(true);
    out_m->SetGain(0.3);
    mp3 = new AudioGeneratorMP3();
    mp3->begin(id3, out_m);
    button_clicked = false;
    while(mp3->isRunning()){
     if (!mp3->loop()) mp3->stop();
     }
  }
}
