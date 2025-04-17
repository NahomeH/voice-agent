import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set absolute path for Google Application Credentials
cwd = os.getcwd()
if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    google_creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_creds_path.startswith('/') and not google_creds_path.startswith(cwd):
        # If path is absolute but doesn't start with current directory, make it absolute
        if not os.path.isfile(google_creds_path):
            absolute_path = os.path.join(cwd, google_creds_path.lstrip('/'))
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = absolute_path
            print(f"Set GOOGLE_APPLICATION_CREDENTIALS to absolute path: {absolute_path}")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

# Audio Settings
AUDIO_RATE = 16000  # Audio sample rate in Hz
AUDIO_CHUNK = int(AUDIO_RATE / 10)  # 100ms chunks
TTS_SAMPLE_RATE = 48000  # Higher sample rate for output audio quality

# LLM Settings
LLM_MODEL = "gpt-4o-mini"  # OpenAI model to use
TEMPERATURE = 0.7  # Creativity level (0.0-1.0)
MAX_TOKENS = 2048  # Maximum response length

# Voice Settings
VOICE_LANGUAGE = "en-US"
VOICE_NAME_FEMALE = "en-US-Neural2-F"  # Default female voice
VOICE_NAME_MALE = "en-US-Neural2-J"    # Default male voice
DEFAULT_VOICE_GENDER = "FEMALE"        # Default gender preference

# Application Settings
LOG_LEVEL = "INFO"

# Therapy Assistant System Prompt
SYSTEM_PROMPT = """
You are a compassionate AI therapy assistant designed to provide supportive conversations.
Listen carefully to the user's concerns and respond with empathy and understanding.
Ask open-ended questions to encourage reflection.
If the user is in crisis, provide appropriate resources and encourage them to seek professional help.
"""