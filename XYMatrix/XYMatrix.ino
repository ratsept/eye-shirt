// Use if you want to force the software SPI subsystem to be used for some reason (generally, you don't)
// #define FASTLED_FORCE_SOFTWARE_SPI
// Use if you want to force non-accelerated pin access (hint: you really don't, it breaks lots of things)
// #define FASTLED_FORCE_SOFTWARE_SPI
// #define FASTLED_FORCE_SOFTWARE_PINS
#include "FastLED.h"

///////////////////////////////////////////////////////////////////////////////////////////
//
// Move a white dot along the strip of leds.  This program simply shows how to configure the leds,
// and then how to turn a single pixel white and then off, moving down the line of pixels.
// 

// How many leds are in the strip?
#define NUM_LEDS 100

// Data pin that led data will be written out over
#define DATA_PIN 11

// Clock pin only needed for SPI based chipsets when not using hardware SPI
//#define CLOCK_PIN 8

// This is an array of leds.  One item for each led in your strip.
CRGB leds[NUM_LEDS];

boolean wifi_connected = false;
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// This function sets up the ledsand tells the controller about them
void setup() {
  Serial.begin(115200);
  inputString.reserve(200);
  
  // sanity check delay - allows reprogramming if accidently blowing power w/leds
  delay(2000);

  FastLED.addLeds<WS2812, DATA_PIN, RGB>(leds, NUM_LEDS);
}

// This function runs over and over, and is where you do the magic to light
// your leds.
void loop()
{
  Serial.println("loop");
  // Move a single white led 
  for(int whiteLed = 0; whiteLed < NUM_LEDS; whiteLed = whiteLed + 1) {
    if(stringComplete)
    {
       if(inputString == "OPEN")
       {
           Serial.println("tere!!!");
           while(true);
       }
    }
    // Turn our current led on to white, then show the leds
    leds[whiteLed] = CRGB(255,255,255);

    // Show the leds (only one of which is set to white, from above)
    FastLED.show();

    // Wait a little bit
    //delay(100);

    // Turn our current led back to black for the next loop around
    leds[whiteLed] = CRGB::Black;
  }
}
/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  static boolean receiving_status = false;
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    if(!wifi_connected)
    {
      // add it to the inputString:
      //inputString += inChar;
      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == '*' && !receiving_status) {
        receiving_status = true;
        inputString="";
      }
      else if (inChar == '*' && receiving_status)
      {
        receiving_status = false;
        stringComplete = 1;
      }
      else if(receiving_status)
      {
        inputString += inChar;
      }
    } 
  }
}
