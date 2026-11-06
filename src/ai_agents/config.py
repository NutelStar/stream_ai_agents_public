import os

BACKUP_FILE = "ChatHistoryBackup.txt"
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "ai_images")
AI_IMAGE = "AI Image"
AUDIO_INPUT = "Code Audio"
OBS_SOURCES = {
    "scenes": ("Live", "Just Chatting Screen", "Live Block View"),
    "filters": ("", " Chat", " Block"),
}
WAIT_AI_GONE = 1

AUDIO_OUTPUT_NAME = "CABLE Input"
DECIBELS_GAIN = 0
