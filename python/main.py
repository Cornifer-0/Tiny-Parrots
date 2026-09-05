import time

from arduino.app_utils import App, Bridge
from utils import play_audio, record_frame, record_audio, stop_recording


print("Hello world!")


def loop():
    """This function is called repeatedly by the App framework."""
    # You can replace this with any code you want your App to run repeatedly.
    time.sleep(0.1)


def on_button_event(but):
    if but == "A_pressed":
        play_audio()
    elif but == "B_pressed":
        record_frame()
    elif but == "C_pressed":
        record_audio()
    elif but == "C_released":
        stop_recording()
    

Bridge.notify("set_status", "idle")

Bridge.provide("button_event", on_button_event)

# See: https://docs.arduino.cc/software/app-lab/tutorials/getting-started/#app-run
App.run(user_loop=loop)
