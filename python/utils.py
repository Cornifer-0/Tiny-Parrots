import os
import re
import time
import signal
import subprocess
from pathlib import Path
import cv2
from arduino.app_utils import App, Bridge

# Permanent ALSA Hardware
PLAYBACK_HW = "plughw:CARD=EarPods,DEV=0"
PLAYBACK_CARD = "EarPods"
RECORD_HW = "plughw:CARD=B105,DEV=0"
RECORD_CARD = "B105"

# Directoris
APP_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = APP_DIR / "audio"
FOTOS_DIR = APP_DIR / "fotos"

audio_veu = AUDIO_DIR / "veu.wav"
audio_beep = AUDIO_DIR / "beep.wav"

last_trigger_time = 0
COOLDOWN_SECONDS = 1.0

# Stat de gravacio
_proc_audio = None
_audio_output_path = audio_veu


#  CAMERA  

""" Fa una foto i la guarda a la carpeta de fotos"""
""" Retorna {bool, string} true si hi ha exit, retorna on s'ha guardat o l'error que hi ha hagut"""

"Mirem tots els possibles fitxers on linux hauria pogut assignar la camera /dev/video0-2"

def record_frame(output_path="/app/fotos/foto.jpg"):
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    for idx in range(3):
        cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
        if not cap.isOpened():
            cap.release()
            continue

        # Posar MJPEG resolution
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # S'ha de deixar temps a que el sensor de llum tinc exposicio
        time.sleep(0.5)
        valid_frame = None
        for _ in range(5):
            ret, frame = cap.read()
            if ret and frame is not None and frame.size > 0:
                valid_frame = frame

        cap.release()

        if valid_frame is not None:
            cv2.imwrite(str(out_file), valid_frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"[CAM LOG] Foto guardada a {out_file} ({out_file.stat().st_size} bytes) des de /dev/video{idx}")
            return True, str(out_file)

    print("[CAM LOG] Error: No s'ha pogut obrir la càmera a /dev/video0-2")
    return False, "Càmera no trobada"


#  AUDIO PLAYBACK

"""Troba la card que es pot reproduir sorolll"""

def _play_wav_aplay(file_path):
    # Unmute controls
    try:
        subprocess.run(
            ["amixer", "-c", PLAYBACK_CARD, "sset", "PCM", "100%", "unmute"],
            capture_output=True, timeout=1
        )
    except Exception as ex:
        print(f"[AUDIO LOG] Avís en ajustar volum: {ex}")

    # Play audio stream via plughw
    cmd = ["aplay", "-D", PLAYBACK_HW, str(file_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0

def play_audio():
    Bridge.notify("set_status", "playing")
    try:
        if audio_veu.exists():
            print(f"[AUDIO LOG] Intentant reproduir: {audio_veu}")
            _play_wav_aplay(audio_veu)
        elif audio_beep.exists():
            print(f"[AUDIO LOG] Intentant reproduir: {audio_beep}")
            _play_wav_aplay(audio_beep)
        else:
            print(f"[AUDIO LOG] No hi ha cap fitxer d'àudio a {AUDIO_DIR}")
    except Exception as e:
        print(f"[AUDIO LOG] Excepció en play_audio: {e}")

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

    # Forcem 2 canals (Estèreo) i 48000Hz (format natiu del micròfon Logitech)
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
