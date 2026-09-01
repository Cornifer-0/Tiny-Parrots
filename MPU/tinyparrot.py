import cv2;
import pyaudio
import wave
from arduino_bridge import Bridge
from edge_impulse_linux.image import ImageImpulseRunner


# Load the model
runner = ImageImpulseRunner("model/parrot_model.eim")
runner.init()


# Grab the first camera
camera = cv2.VideoCapture(0)


# Just debugging for now
def on_button_event(state):
    if state == "pressed":
        print("Recording audio...")
    elif state == "realased":
        print("Saving audio...")


# Connect to MCU bridge listener
bridge = Bridge()
bridge.on("button_event", on_button_event)


while True:
    # Keep checking MCU events
    bridge.poll() # 


    #TODO: Add the image recognition things...