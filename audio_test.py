import os
import time
import sounddevice as sd
import numpy as np
import pyaudio
from google.cloud import speech, texttospeech

# Set absolute path for Google credentials
cwd = os.getcwd()
credentials_file = 'henry-457117-64cc150bdce6.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(cwd, credentials_file)

from audio.input import MicrophoneStream, get_speech_client, get_streaming_config
from audio.output import text_to_speech
from config import AUDIO_RATE, AUDIO_CHUNK, TTS_SAMPLE_RATE

def test_recording(duration=5):
    """Test recording audio for a specified duration."""
    print(f"\n--- Testing Audio Recording ({duration} seconds) ---")
    
    # Create an array to store audio data
    frames = []
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Open stream
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=AUDIO_RATE,
        input=True,
        frames_per_buffer=AUDIO_CHUNK
    )
    
    print(f"Recording for {duration} seconds...")
    
    # Record for the specified duration
    for i in range(0, int(AUDIO_RATE / AUDIO_CHUNK * duration)):
        data = stream.read(AUDIO_CHUNK)
        frames.append(data)
    
    print("Recording finished.")
    
    # Close resources
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return b''.join(frames)

def test_playback(audio_data):
    """Test playing back audio data."""
    print("\n--- Testing Audio Playback ---")
    
    # Convert bytes to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Normalize audio
    audio_normalized = audio_array.astype(np.float32) / 32767.0
    
    # Play audio
    print("Playing back recorded audio...")
    sd.play(audio_normalized, AUDIO_RATE)
    sd.wait()
    print("Playback finished.")

def test_speech_to_text(audio_data):
    """Test converting speech to text using Google Cloud."""
    print("\n--- Testing Speech-to-Text ---")
    
    try:
        client = get_speech_client()
        
        # Configure audio
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=AUDIO_RATE,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
        
        # Send request
        print("Transcribing audio...")
        response = client.recognize(config=config, audio=audio)
        
        # Process results
        if not response.results:
            print("No speech detected.")
            return None
        
        transcription = response.results[0].alternatives[0].transcript
        confidence = response.results[0].alternatives[0].confidence
        
        print(f"Transcription: {transcription}")
        print(f"Confidence: {confidence:.2f}")
        
        return transcription
        
    except Exception as e:
        print(f"Error in speech-to-text: {e}")
        return None

def test_text_to_speech(text="Hello, this is a test of the text to speech system."):
    """Test converting text to speech using Google Cloud."""
    print("\n--- Testing Text-to-Speech ---")
    
    try:
        # Convert text to speech
        print(f"Converting text to speech: '{text}'")
        audio_content = text_to_speech(text)
        
        if not audio_content:
            print("Failed to generate audio content.")
            return
        
        # Convert bytes to numpy array (adjust for LINEAR16 encoding)
        audio_array = np.frombuffer(audio_content, dtype=np.int16)
        
        # Normalize audio
        audio_normalized = audio_array.astype(np.float32) / 32767.0
        
        # Play audio
        print("Playing audio...")
        sd.play(audio_normalized, TTS_SAMPLE_RATE)
        sd.wait()
        print("Playback finished.")
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def main():
    print("\n=== Audio Testing Suite ===\n")
    
    # Test recording
    audio_data = test_recording(5)
    
    # Test playback of recorded audio
    test_playback(audio_data)
    
    # Test speech-to-text
    transcription = test_speech_to_text(audio_data)
    
    # Test text-to-speech (either with transcription or default text)
    if transcription:
        test_text_to_speech(transcription)
    else:
        test_text_to_speech()
    
    print("\n=== Audio Testing Complete ===")

if __name__ == "__main__":
    main() 