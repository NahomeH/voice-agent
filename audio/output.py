# audio/output.py
import logging
import numpy as np
import sounddevice as sd
from google.cloud import texttospeech

from config import (
    TTS_SAMPLE_RATE,
    VOICE_LANGUAGE,
    VOICE_NAME_FEMALE,
    VOICE_NAME_MALE,
    DEFAULT_VOICE_GENDER
)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_tts_client():
    """Initialize and return the Google Text-to-Speech client."""
    try:
        return texttospeech.TextToSpeechClient()
    except Exception as e:
        logger.error(f"Failed to initialize Text-to-Speech client: {e}")
        raise

def text_to_speech(text, voice_gender=DEFAULT_VOICE_GENDER):
    """
    Convert text to speech using Google Cloud TTS.
    
    Args:
        text (str): Text to convert to speech
        voice_gender (str): 'MALE' or 'FEMALE' to determine voice
        
    Returns:
        bytes: Audio content as bytes
    """
    try:
        client = get_tts_client()
        
        # Select voice based on gender preference
        voice_name = VOICE_NAME_FEMALE if voice_gender == "FEMALE" else VOICE_NAME_MALE
        
        # Configure audio settings
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=TTS_SAMPLE_RATE
        )
        
        # Configure voice
        voice = texttospeech.VoiceSelectionParams(
            language_code=VOICE_LANGUAGE,
            name=voice_name
        )
        
        # Prepare input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Generate speech
        logger.info(f"Converting text to speech using voice {voice_name}")
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        return response.audio_content
        
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {e}")
        return None

def play_audio(audio_content):
    """
    Play audio from bytes content.
    
    Args:
        audio_content (bytes): Audio content to play
        
    Returns:
        bool: True if playback successful, False otherwise
    """
    if not audio_content:
        logger.error("No audio content to play")
        return False
    
    try:
        # Convert audio content to numpy array
        audio = np.frombuffer(audio_content, dtype=np.int16)
        
        # Play the audio and wait until it finishes
        logger.info("Playing audio response")
        sd.play(audio, TTS_SAMPLE_RATE)
        sd.wait()
        return True
        
    except Exception as e:
        logger.error(f"Error playing audio: {e}")
        return False

def speak_text(text, voice_gender=DEFAULT_VOICE_GENDER):
    """
    Convert text to speech and play it.
    
    Args:
        text (str): Text to speak
        voice_gender (str): 'MALE' or 'FEMALE' to determine voice
        
    Returns:
        bool: True if successful, False otherwise
    """
    audio_content = text_to_speech(text, voice_gender)
    if audio_content:
        return play_audio(audio_content)
    return False