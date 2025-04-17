# audio/input.py
import queue
import pyaudio
from google.cloud import speech
import os
import logging

from config import AUDIO_RATE, AUDIO_CHUNK, VOICE_LANGUAGE

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate=AUDIO_RATE, chunk=AUDIO_CHUNK):
        """Initialize audio stream parameters."""
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        """Set up the audio stream when entering the context."""
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,  # Mono audio
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        """Clean up resources when exiting the context."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Callback to continuously collect data from the audio stream."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """Generate audio chunks from the stream."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Consume all buffered data
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def get_speech_client():
    """Initialize and return the Google Speech-to-Text client."""
    try:
        return speech.SpeechClient()
    except Exception as e:
        logger.error(f"Failed to initialize Speech-to-Text client: {e}")
        raise


def get_streaming_config():
    """Create speech recognition configuration for streaming audio."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=AUDIO_RATE,
        language_code=VOICE_LANGUAGE,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=False,
        single_utterance=True,
    )
    return streaming_config


def get_transcription(responses):
    """Process speech recognition responses to get the final transcription."""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            logger.info(f"Final transcript: {transcript}")
            return transcript
    
    return ""


def record_and_transcribe():
    """
    Record audio from microphone and convert to text.
    
    Returns:
        str: Transcribed text from speech
    """
    logger.info("Listening for speech...")
    
    try:
        client = get_speech_client()
        streaming_config = get_streaming_config()
        
        with MicrophoneStream() as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )
            
            responses = client.streaming_recognize(streaming_config, requests)
            transcription = get_transcription(responses)
            
            if not transcription.strip():
                logger.info("No speech detected")
                return ""
            
            return transcription
            
    except Exception as e:
        logger.error(f"Error in speech recognition: {e}")
        return ""