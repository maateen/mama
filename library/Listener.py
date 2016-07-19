import os

import wave

import pyaudio


class Listener():
    """
    @description: This class will record the voice as wav.
    """

    def __init__(self, config, pid):
        audio_chunk = config['audio_chunk']
        audio_format = pyaudio.paInt16  # paInt8
        audio_channels = config['audio_channels']
        audio_rate = config['audio_rate']
        recording_time = config['recording_time']
        wav_file_path = "/tmp/mama/output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=audio_format,
                        channels=audio_channels,
                        rate=audio_rate,
                        input=True,
                        frames_per_buffer=audio_chunk)  # buffer

        # we play a sound to signal the start
        parent_dir = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
        os.system('play ' + parent_dir + 'resources/sound.wav')
        print("* recording")
        os.system('touch /tmp/mama/mama_start_' + pid)

        frames = []

        for i in range(0, int(audio_rate / audio_chunk * recording_time)):
            data = stream.read(audio_chunk)
            frames.append(data)  # 2 bytes(16 bits) per channel

        print("* done recording")
        os.system('touch /tmp/mama/mama_record_complete_' + pid)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(wav_file_path, 'wb')
        wf.setnchannels(audio_channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(audio_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
