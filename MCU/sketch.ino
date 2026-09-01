// Arduino microcontroller code for the MCU

#include <ArduinoBridge.h>

const int BUTTON_PIN = 2;
bool lastState = HIGH;

void SetUp()
{
    Bridge.begin();
    pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop()
{
    bool currentState = digitalRead(BUTTON_PIN);

    if (currentState != lastState)
    {
        if (currentState == LOW)
        {
            Bridge.notify("button_event", "pressed");
        }
        else
        {
            Bridge.notify("button_event", "released");
        }
        lastState = currentState;
    }
    delay(20);
}