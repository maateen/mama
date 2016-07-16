import wave
from os import system

import pyaudio


class Listener():
    """
    @description: This class will record the voice as wav.
    """

    def __init__(self, pid):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16  # paInt8
        CHANNELS = 2
        RATE = 8000  # sample rate
        RECORD_SECONDS = 3
        WAV_FILE_PATH = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # buffer

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)  # 2 bytes(16 bits) per channel

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAV_FILE_PATH, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        system('> /tmp/mama/mama_stop_' + pid)
