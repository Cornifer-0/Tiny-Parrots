import time
import signal
import subprocess
from pathlib import Path
import cv2
from arduino.app_utils import Bridge
import random

PLAYBACK_HW = "plughw:CARD=EarPods,DEV=0"
PLAYBACK_CARD = "EarPods"
RECORD_HW = "plughw:CARD=B105,DEV=0"
RECORD_CARD = "B105"

# Directoris
APP_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_DIR / "audio"
FOTOS_DIR = APP_DIR / "fotos"

audio_veu = AUDIO_DIR / "veu.wav"
audio_beep = AUDIO_DIR / "prerecorded_ai_voice/what_is_that.wav"
audio_beep2 = AUDIO_DIR / "prerecorded_ai_voice/teach_me.wav"

last_trigger_time = 0
COOLDOWN_SECONDS = 1.0

# Stat de gravacio
_proc_audio = None
_audio_output_path = audio_veu


#  CAMERA  

"Mirem tots els possibles fitxers on linux hauria pogut assignar la camera /dev/video0-2"
"Aquesta funcion nomes s'executa completa una vegada ( la primera ) despres es guarda el fitxer de la camera a GLOBAL_CAP"

GLOBAL_CAP = None
def _get_camera_handle():
    global GLOBAL_CAP
    
    if GLOBAL_CAP is not None and GLOBAL_CAP.isOpened():
        return GLOBAL_CAP

    for idx in range(3):
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if not cap.isOpened():
            cap.release()
            continue

        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        for _ in range(20):
            cap.read()

        ret, frame = cap.read()
        if ret and frame is not None and frame.size > 0:
            print(f"[CAM LOG] Càmera inicialitzada correctament a /dev/video{idx}")
            GLOBAL_CAP = cap
            return GLOBAL_CAP
        
        cap.release()

    print("[CAM LOG] Error: No s'ha pogut obrir la càmera a /dev/video0-2")
    return None



""" Fa una foto i la retorna"""
def record_frame():
    Bridge.notify("set_status", "happy")

    cap = _get_camera_handle()
    if cap is None:
        Bridge.notify("set_status", "idle")
        return None

    for _ in range(4):
        cap.grab()

    ret, frame = cap.read()

    Bridge.notify("set_status", "idle")

    if ret and frame is not None and frame.size > 0:

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE) # The camera is physically rotated 90 degrees, so we have to correct it.
        
        out_file = Path("/app/fotos/foto.jpg")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_file), frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
        return frame

    return None


    
#  AUDIO PLAYBACK

"""Troba la card que es pot reproduir sorolll"""

def _play_wav_aplay(file_path):
    # Unmute controls
    """
    try:
        subprocess.run(
            ["amixer", "-c", PLAYBACK_CARD, "sset", "PCM", "100%", "unmute"],
            capture_output=True, timeout=1
        )
    except Exception as ex:
        print(f"[AUDIO LOG] Avís en ajustar volum: {ex}")
    """
    
    cmd = ["aplay", "-D", PLAYBACK_HW, str(file_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0

def play_audio(filename=None):
    Bridge.notify("set_status", "playing")
    try:
        target_file = None

        if filename:
            # Ensure .wav extension
            wav_name = filename if filename.endswith(".wav") else f"{filename}.wav"
            candidate = AUDIO_DIR / wav_name
            
            if candidate.exists():
                target_file = candidate
            else:
                print(f"[AUDIO LOG] Fitxer especificat no trobat: {candidate}")

        if not target_file:
            if audio_beep.exists() and random.random() > 0.5:
                target_file = audio_beep
            else:
                target_file = audio_beep2

        if target_file and target_file.exists():
            #print(f"[AUDIO LOG] Intentant reproduir: {target_file}")
            _play_wav_aplay(target_file)
        else:
            print(f"[AUDIO LOG] No hi ha cap fitxer d'àudio vàlid a {AUDIO_DIR}")

    except Exception as e:
        print(f"[AUDIO LOG] Excepció en play_audio: {e}")
    finally:
        Bridge.notify("set_status", "idle")

#  AUDIO RECORDING

def _unmute_mic():
    subprocess.run(["amixer", "-c", RECORD_CARD, "sset", "Mic", "100%", "unmute", "cap"], capture_output=True)
    subprocess.run(["amixer", "-c", RECORD_CARD, "sset", "Capture", "100%", "unmute", "cap"], capture_output=True)

def record_audio(output_path=str(audio_veu)):
    global _proc_audio, _audio_output_path
    _audio_output_path = Path(output_path)
    _audio_output_path.parent.mkdir(parents=True, exist_ok=True)

    if _proc_audio is not None and _proc_audio.poll() is None:
        print("[REC LOG] Ja hi ha una gravacio en curs")
        return False, "Ja hi ha una gravacio en curs"

    if _audio_output_path.exists():
        _audio_output_path.unlink(missing_ok=True)

    _unmute_mic()

    cmd = [
        "arecord", "-D", RECORD_HW,
        "-t", "wav", "-f", "S16_LE", "-r", "48000", "-c", "2",
        str(_audio_output_path)
    ]

    try:
        _proc_audio = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        time.sleep(0.3)
        if _proc_audio.poll() is not None:
            _, err = _proc_audio.communicate()
            _proc_audio = None
            print(f"[REC LOG] Error arecord: {err.strip()}")
            return False, f"Error: {err.strip()}"

        print(f"[REC LOG] Gravacio iniciada amb '{RECORD_CARD}' -> {_audio_output_path}")
        return True, "Gravacio iniciada"
    except Exception as e:
        _proc_audio = None
        print(f"[REC LOG] Excepció: {e}")
        return False, str(e)

def stop_recording():
    global _proc_audio, _audio_output_path

    Bridge.notify("set_status", "idle")
    
    if _proc_audio is None or _proc_audio.poll() is not None:
        _proc_audio = None
        print("[REC LOG] No hi havia cap gravació activa")
        return False, "Cap gravació activa"

    _proc_audio.send_signal(signal.SIGINT)
    try:
        _proc_audio.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        _proc_audio.kill()

    _proc_audio = None

    if _audio_output_path and _audio_output_path.exists() and _audio_output_path.stat().st_size > 0:
        print(f"[REC LOG] Àudio finalitzat i guardat a {_audio_output_path} ({_audio_output_path.stat().st_size} bytes)")
        return True, str(_audio_output_path)

    print("[REC LOG] Error: Fitxer audio buit o no generat")
    return False, "Fitxer audio buit o no generat"

# Speaking text

TEMP_TTS_WAV = Path("/tmp/tts_parrot.wav")

# Not in use
def speak_text(text, pitch=90, speed=160): 
    """Generates an offline synthetic parrot voice and plays it via aplay."""
    try:
        cmd_synth = [
            "espeak-ng",
            "-p", str(pitch), 
            "-s", str(speed), 
            "-w", str(TEMP_TTS_WAV),
            text
        ]
        res = subprocess.run(cmd_synth, capture_output=True, text=True)
        
        if res.returncode != 0:
            print(f"[TTS ERROR] Failed to synthesize: {res.stderr}")
            return False

        print(f"[TTS LOG] Speaking: '{text}'") 
        return _play_wav_aplay(TEMP_TTS_WAV)

    except Exception as e:
        print(f"[TTS LOG] Exception during speak_text: {e}")
        return False
