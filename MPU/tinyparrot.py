import cv2;
import pyaudio
import wave
from arduino_bridge import Bridge
from edge_impulse_linux.image import ImageImpulseRunner


runner = ImageImpulseRunner("model/parrot_model.eim")
runner.init()