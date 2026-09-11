import time

from pathlib import Path

from arduino.app_utils import App, Bridge
from python.utils import play_audio, record_frame, record_audio, stop_recording, speak_text
from python.vision import classify_image
import random

from edge_impulse_linux.image import ImageImpulseRunner


GENERIC_PARROT_PHRASES = [
    "Squawk! Polly wants an air-gapped cracker!",
    "Who's a smart AI? I am! Squawk!",
    "100 percent local processing, 100 percent private!",
    "Shh... don't tell the cloud, but I'm completely offline!",
    "Your data stays right here on this board. Zero uploads!",
    "No internet? No problem! Air-gapped and proud!",
    "Ooh, interesting! What do we have here?",
    "Aha! My local neural net sees something!",
    "Feathers fluffed and camera ready!",
    "Flap flap, beep boop, squawk!"
]


#print("Hello world!")

last_speak_time = time.time()
next_speak_interval = random.randint(10, 20)

last_recognized_object = "None"



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

                    article = "an" if result[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
    
                    # Synthesize "This is a" or "This is an"
                    speak_text(f"This is {article}")
                    
                    play_audio(result)

                    last_recognized_object = result
                    last_object_speak_time = time.time()
            else:
                # Reset when no object is in front of the camera
                print("Don't see nothing")

            if current_time - last_speak_time >= next_speak_interval:
                phrase = get_random_parrot_phrase()
                speak_text(phrase)
                last_speak_time = current_time
                next_speak_interval = random.randint(15, 25)

            time.sleep(0.05)




def on_button_event(but):    
    global last_recognized_object
    if but == "C_pressed":

        if(last_recognized_object == "None"):
            play_audio("beep")
            speak_text("Show me something first!")
            return
            
        path_audio = Path(f"/app/audio/{last_recognized_object}.wav")
        record_audio(str(path_audio))
    if but == "C_released":
        stop_recording()


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

# See: https://docs.arduino.cc/software/app-lab/tutorials/getting-started/#app-run
App.run(user_loop=loop)
