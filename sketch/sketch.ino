#include "Arduino_RouterBridge.h"
#include <Arduino_Modulino.h>
#include "Arduino_LED_Matrix.h"

ArduinoLEDMatrix matrix;
ModulinoButtons buttons;

bool lastA = false;
bool lastB = false;
bool lastC = false;

uint8_t frame_rec[8][12] = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}};

uint8_t frame_play[8][12] = {
    {0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0}};

uint8_t frame_idle[8][12] = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}};

void set_status(String status)
{
    if (status == "recording")
    {
        matrix.renderBitmap(frame_rec, 8, 12);
    }
    else if (status == "playing")
    {
        matrix.renderBitmap(frame_play, 8, 12);
    }
    else
    {
        matrix.renderBitmap(frame_idle, 8, 12);
    }
}

void setup()
{
    Bridge.begin();
    delay(100);

    matrix.begin();
    matrix.renderBitmap(frame_idle, 8, 12);

    Bridge.provide("set_status", set_status);

    Modulino.begin(Wire1);
    buttons.begin();
}

void loop()
{
    buttons.update();

    bool currentA = buttons.isPressed(0);
    bool currentB = buttons.isPressed(1);
    bool currentC = buttons.isPressed(2);

    if (currentA != lastA)
    {
        if (currentA)
            Bridge.notify("button_event", "A_pressed");
        else
            Bridge.notify("button_event", "A_released");
        lastA = currentA;
    }

    if (currentB != lastB)
    {
        if (currentB)
            Bridge.notify("button_event", "B_pressed");
        else
            Bridge.notify("button_event", "B_released");
        lastB = currentB;
    }

    if (currentC != lastC)
    {
        if (currentC)
            Bridge.notify("button_event", "C_pressed");
        else
            Bridge.notify("button_event", "C_released");
        lastC = currentC;
    }

    delay(20);
}