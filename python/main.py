import time

from pathlib import Path

from arduino.app_utils import App, Bridge
from utils import play_audio, record_frame, record_audio, stop_recording, speak_text
from vision import classify_image
import random

from edge_impulse_linux.image import ImageImpulseRunner

# Self-healing check for headless OpenCV


GENERIC_PARROT_PHRASES = [
    "cool",
    "fascinating",
    "hmmm",
    "privacy",
    "privacy1",
    "qualcomm1",
    "squak3",
    "upc1",
    "upc2",
]

BEFORE_OBJECT_PHRASES = [
    "i_see_a",
    "this_is_a"
]

EATING_PHRASES = [
    "eat0",
    "eat1",
    "eat2",
    "eat3"
]



#print("Hello world!")

last_speak_time = time.time()
next_speak_interval = random.randint(10, 20)

last_recognized_object = "None"

APP_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_DIR / "audio"



def loop():    
    global last_speak_time, next_speak_interval, last_recognized_object

    model_path = "/app/model.eim"

    last_object_speak_time = 0
    OBJECT_COOLDOWN = 6.0

    with ImageImpulseRunner(model_path) as runner:
        runner.init()
        print("Successfully loaded vision model")


        while True:
            current_time = time.time()

            frame = record_frame()
            print("record frame!")

            result = classify_image(runner, frame, confidence_threshold=0.70)

            if result and result != "Error":
                # Only speak if it's a new object or the cooldown timer expired
                is_new_object = (result != last_recognized_object)
                cooldown_passed = (current_time - last_object_speak_time > OBJECT_COOLDOWN)

                if is_new_object or cooldown_passed:
                    print(f"[AI DETECTED] {result} -> Announcing!")

                    have_it_path = AUDIO_DIR / f"{result}.wav"

                    phrase = random.choice(BEFORE_OBJECT_PHRASES)
                    if have_it_path.exists():
                        play_audio(f"prerecorded_ai_voice/{phrase}")
                    
                    play_audio(result)

                    if have_it_path.exists() and random.random() > 0.3:
                        play_audio("prerecorded_ai_voice/right_question")

                    last_recognized_object = result
                    last_object_speak_time = time.time()
            else:
                # Reset when no object is in front of the camera
                print("Don't see nothing")

            if current_time - last_speak_time >= next_speak_interval:
                phrase = random.choice(GENERIC_PARROT_PHRASES)
                play_audio(f"prerecorded_ai_voice/{phrase}")
                last_speak_time = current_time
                next_speak_interval = random.randint(15, 25)

            time.sleep(0.05)




def on_button_event(but):    
    global last_recognized_object
    if but == "B_pressed":

        if(last_recognized_object == "None"):
            play_audio("beep")
            speak_text("Show me something first!")
            return
            
        path_audio = Path(f"/app/audio/{last_recognized_object}.wav")
        record_audio(str(path_audio))
    elif but == "B_released":
        stop_recording()
    elif but == "C_pressed":
        phrase = random.choice(EATING_PHRASES)
        play_audio(f"prerecorded_ai_voice/{phrase}")
    


def get_random_parrot_phrase():
    return random.choice(GENERIC_PARROT_PHRASES)

""" Testing periferials#
def on_button_event(but):
    if but == "A_pressed":
        play_audio()
    elif but == "B_pressed":
        record_frame()
    elif but == "C_pressed":
        record_audio()
    elif but == "C_released":
        stop_recording()
""" 

Bridge.notify("set_status", "idle")

Bridge.provide("button_event", on_button_event)

play_audio("prerecorded_ai_voice/awake_and_ready")

# See: https://docs.arduino.cc/software/app-lab/tutorials/getting-started/#app-run
App.run(user_loop=loop)
