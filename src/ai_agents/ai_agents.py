import argparse
import time
import keyboard
import os
from rich import print
from .azure_speech_to_text import SpeechToTextManager
from .openai_chat import OpenAiManager
from .eleven_labs import ElevenLabsManager
from .audio_player import AudioManager
from .ai_prompts import SWEETEL
from .config import (
    AI_IMAGE,
    AUDIO_INPUT,
    BACKUP_FILE,
    IMAGE_PATH,
    OBS_SOURCES,
    WAIT_AI_GONE,
)

def setVisibilityObs(obs_manager, filter_name: str, filter_ai: str, audio_input: str, state_filter: bool, state_ai: bool, all_scenes = False):
    # Show AI sources, as well as starting the animations
    if all_scenes:
        for scene in OBS_SOURCES["scenes"]:
            if state_ai:
                obs_manager.set_source_visibility(scene, AI_IMAGE, state_ai)
            obs_manager.set_filter_visibility(scene, filter_name, state_filter)
    else:
        if state_ai:
            obs_manager.set_source_visibility(obs_manager.get_scene(), AI_IMAGE, state_ai)
        obs_manager.set_filter_visibility(obs_manager.get_scene(), filter_name, state_filter)

    # Activate audio filters for source movement
    for filter in OBS_SOURCES["filters"]:
        obs_manager.set_filter_visibility(audio_input, filter_ai + filter, state_filter)

    # If we hide AI, we hate until the animation finishes
    if not state_ai:
        time.sleep(WAIT_AI_GONE)
        for scene in OBS_SOURCES["scenes"]:
            obs_manager.set_source_visibility(scene, AI_IMAGE, state_ai)

def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the voice-driven AI assistant.")
    parser.add_argument(
        "-obs",
        action="store_true",
        help="run without connecting to OBS or displaying avatar/subtitles",
    )
    args = parser.parse_args(argv)

    elevenlabs_manager = ElevenLabsManager()
    if args.obs:
        from .obs_websockets import OBSWebsocketsManager

        obswebsockets_manager = OBSWebsocketsManager()
    speechtotext_manager = SpeechToTextManager()
    openai_manager = OpenAiManager()
    audio_manager = AudioManager()

    FIRST_SYSTEM_MESSAGE = {"role": "system", "content": SWEETEL['prompt'] + ''' Okay, let the conversation begin!'''}
    openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

    print("[green]Starting the loop, press F4 to begin.")
    while True:
        # Wait until user presses "f4" key
        if keyboard.read_key() != "f4":
            time.sleep(0.1)
            continue

        print("[green]User pressed F4 key! Now listening to your microphone ! Press ctrl+p when you are done.")

        # Get question from mic
        mic_result = speechtotext_manager.speechtotext_from_mic_continuous()

        if mic_result == '':
            print("[red]Did not receive any input from your microphone!")
            continue

        # Send question to OpenAi
        openai_result = openai_manager.chat_with_history(mic_result)

        # Write the results to txt file as a backup
        with open(BACKUP_FILE, "w", encoding="utf-8") as file:
            file.write(str(openai_manager.chat_history))

        # Send it to 11Labs to turn into cool audio
        elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, SWEETEL['voice'], False)

        if args.obs:
            # Enable AI pic in OBS
            image_name = SWEETEL['image_path']
            obswebsockets_manager.set_image(AI_IMAGE, os.path.join(IMAGE_PATH, f"{image_name}.png"))
            setVisibilityObs(obswebsockets_manager, SWEETEL['filter_obs_on'], SWEETEL['filter_obs_audio'], AUDIO_INPUT, True, True)

        # Play the mp3 file
        if args.obs:
            audio_manager.play_audio_louder(elevenlabs_output, False, False, SWEETEL['decibels_gain'])
        else:
            audio_manager.play_audio_louder(elevenlabs_output, True, True, SWEETEL['decibels_gain'])

        if args.obs:
            # Show text in OBS
            from .timestamps import showSentencesOBS

            showSentencesOBS(obswebsockets_manager, openai_result, elevenlabs_output, OBS_SOURCES["scenes"])

            # Delete audio files
            audio_manager.delete_audio_file(elevenlabs_output)
            audio_manager.delete_audio_file(elevenlabs_output.replace(".mp3", "_loud.mp3"))

            # Disable AI pic in OBS
            setVisibilityObs(obswebsockets_manager, SWEETEL['filter_obs_off'], SWEETEL['filter_obs_audio'], AUDIO_INPUT, True, False)

        print("[green]\nFinished processing dialogue.\nReady for next F4 input !\n")


if __name__ == "__main__":
    main()