import os
from google.cloud import texttospeech

# Set absolute path for Google credentials
cwd = os.getcwd()
credentials_file = 'henry-457117-64cc150bdce6.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(cwd, credentials_file)

def list_voices():
    """List available voices from Google Text-to-Speech API."""
    client = texttospeech.TextToSpeechClient()
    
    # List all available voices
    voices = client.list_voices()
    
    # Filter for English voices
    en_voices = [v for v in voices.voices if v.language_codes[0].startswith("en-")]
    
    print(f"\n=== Available English Voices ({len(en_voices)}) ===\n")
    
    # Group by language code
    by_language = {}
    for voice in en_voices:
        lang = voice.language_codes[0]
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(voice)
    
    # Print voices by language
    for lang, voices in sorted(by_language.items()):
        print(f"\n{lang} ({len(voices)} voices):")
        for voice in sorted(voices, key=lambda v: v.name):
            gender = "Female" if voice.ssml_gender == texttospeech.SsmlVoiceGender.FEMALE else "Male"
            print(f"  - {voice.name} ({gender})")
    
    print("\n=== Voice Listing Complete ===")

if __name__ == "__main__":
    list_voices() 