from playsound import playsound


def _play_audio(filename):
    playsound(filename)

def play_audio_async():
    import threading
    sound_filename = 'resources/ding-dong.wav'
    threading.Thread(target=_play_audio, args=(sound_filename,), daemon=True).start()
