# main.py
import os
import sys
import time
import logging
from pynput import keyboard

# Set the absolute path for Google credentials before any other imports
cwd = os.getcwd()
credentials_file = 'henry-457117-64cc150bdce6.json'
credentials_path = os.path.join(cwd, credentials_file)
if os.path.isfile(credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

from config import SYSTEM_PROMPT
from audio.input import record_and_transcribe
from audio.output import speak_text
from processing.llm import LLMProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TherapyAssistant:
    """Main application class for the voice-based therapy assistant."""
    
    def __init__(self):
        """Initialize the therapy assistant."""
        self.llm_processor = LLMProcessor(SYSTEM_PROMPT)
        self.is_recording = False
        self.is_running = True
        self.voice_gender = "MALE"  # Default voice gender
        
    def toggle_recording(self):
        """Toggle recording state."""
        self.is_recording = not self.is_recording
        return self.is_recording
    
    def process_input(self):
        """Record, transcribe, and process user input."""
        print("Listening... (Press any key to stop)")
        
        # Start recording
        transcription = record_and_transcribe()
        
        if not transcription:
            print("No speech detected. Please try again.")
            return
        
        print(f"You: {transcription}")
        
        # Generate response
        response = self.llm_processor.get_response(transcription)
        print(f"Assistant: {response}")
        
        # Convert to speech and play
        speak_text(response, self.voice_gender)
    
    def on_key_press(self, key):
        """Handle key press events."""
        try:
            if key == keyboard.Key.space and not self.is_recording:
                self.is_recording = True
                print("Recording... (Press Space to stop)")
                return True
            
            if key == keyboard.Key.space and self.is_recording:
                self.is_recording = False
                self.process_input()
                return True
                
            if key == keyboard.Key.esc:
                self.is_running = False
                return False
                
        except Exception as e:
            logger.error(f"Error in key press handler: {e}")
    
    def run(self):
        """Run the main application loop."""
        # Display welcome message
        welcome = "Welcome to AI Therapy Assistant. Press Space to start speaking, and ESC to exit."
        print(welcome)
        speak_text("Hello, I'm your therapy assistant. How are you feeling today?", self.voice_gender)
        
        # Set up keyboard listener
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            while self.is_running:
                time.sleep(0.1)  # Prevent high CPU usage
            listener.join()
        
        print("Thank you for using AI Therapy Assistant. Take care!")

if __name__ == "__main__":
    try:
        # Check for API keys
        if not os.environ.get('OPENAI_API_KEY'):
            print("Error: OPENAI_API_KEY not found. Please check your .env file.")
            sys.exit(1)
            
        if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            print("Error: GOOGLE_APPLICATION_CREDENTIALS not found. Please check your .env file.")
            sys.exit(1)
        
        # Start the application
        assistant = TherapyAssistant()
        assistant.run()
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An error occurred: {e}")