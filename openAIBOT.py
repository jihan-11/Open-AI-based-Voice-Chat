import os
from pocketsphinx import LiveSpeech, get_model_path
from gtts import gTTS
import subprocess
import requests  # Requests library for HTTP requests

# Set your OpenAI API key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"

# Initialize the PocketSphinx recognizer
MODELDIR = get_model_path()
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    pocketsphinx_args={
        'hmm': os.path.join(MODELDIR, 'en-us'),
        'lm': os.path.join(MODELDIR, 'en-us.lm.bin'),
        'dic': os.path.join(MODELDIR, 'cmudict-en-us.dict')
    }
)

def get_response(user_input):
    # Example function to interact with OpenAI API (text generation)
    prompt = user_input  # Replace with your prompt logic
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "max_tokens": 50
    }
    response = requests.post("https://api.openai.com/v1/engines/text-davinci-002/completions", headers=headers, json=data)
    response_json = response.json()
    return response_json["choices"][0]["text"].strip()

def recognize_speech_from_mic():
    global speech
    print("Listening...")

    for phrase in speech:
        recognized_text = str(phrase)
        print(f"Recognized: {recognized_text}")
        return recognized_text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("/tmp/output.mp3")  # Save to a temporary file

    # Use mpg321 to play the audio
    subprocess.run(["mpg321", "/tmp/output.mp3"])

def main():
    while True:
        try:
            speech_text = recognize_speech_from_mic()
        except Exception as e:
            print(f"Error recognizing speech: {e}")
            continue
        
        if not speech_text:
            print("Didn't recognize anything.")
            continue
        
        if "jarvis" in speech_text.lower():
            response_from_openai = get_response(speech_text)
            text_to_speech(response_from_openai)
        else:
            print("Didn't recognize 'jarvis'.")

if __name__ == "__main__":
    main()
