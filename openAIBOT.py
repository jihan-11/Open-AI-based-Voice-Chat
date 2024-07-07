import os
from pocketsphinx import LiveSpeech
from gtts import gTTS
import subprocess
import openai  # Import the openai module

# Set your OpenAI API key and customize the chatgpt role
openai.api_key = "xyz"
messages = [{"role": "system", "content": "Your name is Jarvis and give answers in 2 lines"}]

# Define the path to the PocketSphinx acoustic model and language model
MODELDIR = "/usr/share/pocketsphinx/model"
# You might need to adjust MODELDIR based on your system configuration

# Initialize the PocketSphinx recognizer
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(MODELDIR, "en-us"),
    lm=os.path.join(MODELDIR, "en-us.lm.bin"),
    dic=os.path.join(MODELDIR, "cmudict-en-us.dict")
)

def get_response(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})
    # Replace with your logic for OpenAI responses
    ChatGPT_reply = "Placeholder response from OpenAI"
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

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
