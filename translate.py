import os
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\yoges\Downloads\Phase 1\focus-antler-447314-s3-09136432f0a7.json"
# Initialize Google Translate and Text-to-Speech clients
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

# Supported languages for translation and TTS
languages = {
    "en": "English",
    "kn": "Kannada",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "uk": "Ukrainian",
    "ar": "Arabic",
    "ru": "Russian",
    "ja": "Japanese",
}

# Function to translate text
def translate_text(text, target_language):
    if target_language == "en":
        return text  # No translation needed for English
    translation = translate_client.translate(text, target_language=target_language)
    return translation["translatedText"]

# Function to generate audio file from text
def text_to_speech(text, lang_code, output_folder):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"output_{lang_code}.mp3")
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    return output_file

# Function to generate audio files for all supported languages
def generate_audio_files_for_all_languages(text, output_folder="audio_output"):
    audio_files = {}
    for lang_code in languages.keys():
        translated_text = translate_text(text, lang_code)
        audio_file = text_to_speech(translated_text, lang_code, output_folder)
        audio_files[lang_code] = audio_file
    return audio_files

# Example usage
if __name__ == "__main__":
    input_file = "detected_letters.txt"
    output_translation_file = "translations.txt"
    output_audio_folder = "audio_output"

    with open(input_file, "r", encoding="utf-8") as file:
        detected_text = file.read().strip()

        if not detected_text:
            print("The input file is empty. Please provide text.")
            exit()

        print(f"Detected Text: {detected_text}")

        # Save translations
        with open(output_translation_file, "w", encoding="utf-8") as translation_file:
            translation_file.write(f"Original Text: {detected_text}\n\n")

            # Translate and convert to speech for each language
            for lang_code, lang_name in languages.items():
                try:
                    # Translate text
                    translated_text = translate_text(detected_text, lang_code)
                    translation_file.write(f"{lang_name} ({lang_code}): {translated_text}\n")
                    print(f"Translated to {lang_name}: {translated_text}")

                    # Generate speech
                    text_to_speech(translated_text, lang_code, output_audio_folder)
                except Exception as e:
                    print(f"Error with language {lang_name} ({lang_code}): {e}")

        print(f"Translations saved to {output_translation_file}")