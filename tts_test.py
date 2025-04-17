import os
import sys
import time
from audio.output import speak_text

# Set absolute path for Google credentials
cwd = os.getcwd()
credentials_file = 'henry-457117-64cc150bdce6.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(cwd, credentials_file)

def main():
    """Test text-to-speech with different voices and phrases."""
    print("\n=== Text-to-Speech Test ===\n")
    
    # Test female voice
    print("Testing female voice...")
    speak_text("Hello, this is the female voice speaking. How do I sound?", "FEMALE")
    time.sleep(1)
    
    # Test male voice
    print("\nTesting male voice...")
    speak_text("Hello, this is the male voice speaking. How do I sound?", "MALE")
    time.sleep(1)
    
    # Test longer text
    print("\nTesting longer paragraph (female voice)...")
    long_text = (
        "Voice AI has become increasingly sophisticated in recent years. "
        "Modern text-to-speech systems can produce natural-sounding voices "
        "that are often indistinguishable from human speech. "
        "This technology is used in various applications, from virtual assistants "
        "to accessibility tools for people with visual impairments."
    )
    speak_text(long_text, "FEMALE")
    
    print("\n=== Text-to-Speech Test Complete ===")

if __name__ == "__main__":
    main() 