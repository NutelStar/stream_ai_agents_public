from elevenlabs import generate, stream, set_api_key, voices, play, save
import time
import os
from .timestamps import estimate_sentence_timestamps

ELEVENLABS_API = os.getenv('ELEVENLABS_API_KEY')

try:
  set_api_key(ELEVENLABS_API)
except TypeError:
  exit("Ooops! You forgot to set ELEVENLABS_API_KEY in your environment!")

class ElevenLabsManager:

    def __init__(self):
        # CALLING voices() IS NECESSARY TO INSTANTIATE 11LABS FOR SOME FUCKING REASON
        all_voices = voices()
        print(f"\nAll ElevenLabs voices: \n{all_voices}\n")

    # Convert text to speech, then save it to file. Returns the file path
    def text_to_audio(self, input_text, voice="Doug VO Only", save_as_wave=True, subdirectory=""):
        audio_saved = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v2"
        )
        if save_as_wave:
          file_name = f"___Msg{str(hash(input_text))}.wav"
        else:
          file_name = f"___Msg{str(hash(input_text))}.mp3"
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_saved,tts_file)
        return tts_file

    # Convert text to speech, then play it out loud
    def text_to_audio_played(self, input_text, voice="Doug VO Only"):
        audio = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1"
        )
        play(audio)

    # Convert text to speech, then stream it out loud (don't need to wait for full speech to finish)
    def text_to_audio_streamed(self, input_text, voice="Doug VO Only"):
        audio_stream = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1",
          stream=True
        )
        stream(audio_stream)


if __name__ == '__main__':
    elevenlabs_manager = ElevenLabsManager()

    tts_audio = elevenlabs_manager.text_to_audio("This is my streamed test audio. I'm so much cooler than played ! I don't understand this text :/ However, it's pretty cool^^ Nope.", "Sweetel 1")
    timestamps = estimate_sentence_timestamps(tts_audio, "This is my streamed test audio. I'm so much cooler than played ! I don't understand this text :/ However, it's pretty cool^^ Nope.")
    for line in timestamps:
        print(f"{line['start']}s - {line['end']}s: {line['text']}")
    time.sleep(2)
    elevenlabs_manager.text_to_audio_played("This is my played test audio, helo hello", "Sweetel 1")
    time.sleep(2)
    file_path = elevenlabs_manager.text_to_audio("This is my saved test audio, please make me beautiful", "Sweetel 1")
    print("Finished with all tests")

    time.sleep(30)
