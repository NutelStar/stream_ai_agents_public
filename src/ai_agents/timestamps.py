import time
from pydub.utils import mediainfo
from pydub import AudioSegment
from nltk.tokenize import sent_tokenize

def showSentencesOBS(obs_manager, text: str, tts, scenes: list):
    timestamps = estimate_sentence_timestamps(tts, text)

    for scene in scenes:
        obs_manager.set_source_visibility(scene, 'Subtitle Text', True)
    for sentence in timestamps:
        obs_manager.set_text('Subtitle Text', sentence['text'])
        time.sleep(sentence['end'] - sentence['start'])
    for scene in scenes:
        obs_manager.set_source_visibility(scene, 'Subtitle Text', False)

def estimate_sentence_timestamps(audio_path, input_text):
    # Get audio duration
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio) / 1000.0  # convert ms to seconds

    # Break text into sentences
    sentences = sent_tokenize(input_text)

    total_chars = sum(len(s) for s in sentences)
    alignment = []
    time_cursor = 0.0

    for s in sentences:
        proportion = len(s) / total_chars
        duration_s = duration * proportion
        alignment.append({
            "text": s,
            "start": round(time_cursor, 2),
            "end": round(time_cursor + duration_s, 2)
        })
        time_cursor += duration_s

    return alignment