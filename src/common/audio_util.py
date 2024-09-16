import os

from playsound import playsound


def _play_audio(filename):
    playsound(filename)


def play_audio_async():
    import threading
    project_root = os.path.abspath(os.path.dirname(__file__))

    sound_filename = project_root + '/../resources/ding-dong.wav'
    threading.Thread(target=_play_audio, args=(sound_filename,), daemon=True).start()
