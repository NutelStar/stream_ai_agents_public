import pygame
import time
import os
import asyncio
import threading
import logging
from mutagen.mp3 import MP3
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
from .config import AUDIO_OUTPUT_NAME, DECIBELS_GAIN

#########

logger = logging.getLogger(__name__)

#########

class AudioManager:

    def __init__(self):
        # Use higher frequency to prevent audio glitching noises
        # Use higher buffer because why not (default is 512)
        pygame.mixer.init(frequency=48000, buffer=1024)

    def increase_audio_volume(self, file_path, gain_db=DECIBELS_GAIN, deleteFile = False):
        """
        Increases the volume of an audio file.
        """
        sound = AudioSegment.from_file(file_path)
        louder_sound = sound + gain_db  # Increase by X dB
        new_file_path = file_path.replace(".mp3", "_loud.mp3").replace(".wav", "_loud.wav")
        louder_sound.export(new_file_path, format="mp3" if file_path.endswith(".mp3") else "wav")
        if deleteFile:
            os.remove(file_path) # Delete original sound file
        return new_file_path

    def get_output_device_index(self, name_substring):
        """
        Returns the output device index that contains the given substring.
        """
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if dev['max_output_channels'] > 0 and name_substring.lower() in dev['name'].lower():
                print(f"Found {dev['name']} at index {i}")
                return i

        available_devices = [dev["name"] for dev in devices if dev["max_output_channels"] > 0]
        raise RuntimeError(
            f"Could not find an output device containing {name_substring!r}. "
            f"Available output devices: {available_devices}"
        )

    def play_audio(self, file_path, sleep_during_playback=True, delete_file=False):
        """
        Play audio using sounddevice OutputStream so multiple sounds can overlap.
        If sleep_during_playback is False, playback will run in a background thread and this call will return immediately.
        """
        def _play_sync(path, delete_after):
            print(f"Playing file with sounddevice stream: {path}")

            data, fs = sf.read(path, dtype='float32')
            if data.ndim == 1:
                data = data.reshape(-1, 1)

            target_device = self.get_output_device_index(AUDIO_OUTPUT_NAME)

            with sd.OutputStream(
                samplerate=fs,
                channels=data.shape[1],
                device=target_device
            ) as stream:
                stream.write(data)

            if delete_after:
                try:
                    os.remove(path)
                    print(f"Deleted {path}")
                except PermissionError:
                    print(f"Couldn't remove {path}, still in use.")

        if sleep_during_playback:
            _play_sync(file_path, delete_file)
        else:
            def _play_in_background():
                _play_sync(file_path, delete_file)
                
            t = threading.Thread(target=_play_in_background, daemon=True)
            t.start()


    def play_audio_louder(self, file_path, sleep_during_playback = True, delete_file = False, volume_boost_db = DECIBELS_GAIN):
        """
        Play an audio file with an optional volume boost.
        """
        loud_file = self.increase_audio_volume(file_path, volume_boost_db, delete_file)
        self.play_audio(loud_file, sleep_during_playback, delete_file)  # Play the louder file

    async def play_audio_async(self, file_path):
        """
        Parameters:
        file_path (str): path to the audio file
        """
        print(f"Playing file with asynchronously with pygame: {file_path}")
        if not pygame.mixer.get_init(): # Reinitialize mixer if needed
            pygame.mixer.init(frequency=48000, buffer=1024) 
        pygame_sound = pygame.mixer.Sound(file_path) 
        pygame_sound.play()

        # Calculate length of the file, based on the file format
        _, ext = os.path.splitext(file_path) # Get the extension of this file
        if ext.lower() == '.wav':
            wav_file = sf.SoundFile(file_path)
            file_length = wav_file.frames / wav_file.samplerate
            wav_file.close()
        elif ext.lower() == '.mp3':
            mp3_file = MP3(file_path)
            file_length = mp3_file.info.length
        else:
            print("Cannot play audio, unknown file type")
            return

        # We must use asyncio.sleep() here because the normal time.sleep() will block the thread, even if it's in an async function
        await asyncio.sleep(file_length)

    def delete_audio_file(self, file_path):
        """
        Deletes an audio file.
        Parameters:
        file_path (str): path to the audio file
        """
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except PermissionError:
            print(f"Couldn't remove {file_path}, still in use.")