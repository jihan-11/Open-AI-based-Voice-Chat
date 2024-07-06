import os
from pocketsphinx import LiveSpeech
import pyttsx3
import openai

# Initialize pyttsx3
engine = pyttsx3.init()

# Set your OpenAI API key and customize the chatgpt role
openai.api_key = "xyz"
messages = [{"role": "system", "content": "Your name is Jarvis and give answers in 2 lines"}]

# Customizing the output voice
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

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

def main():
    global engine, voices, rate, volume

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
            engine.setProperty('rate', 120)
            engine.setProperty('volume', volume)
            engine.setProperty('voice', voices[0].id)  # Adjust as needed for specific voice
            engine.say(response_from_openai)
            engine.runAndWait()
        else:
            print("Didn't recognize 'jarvis'.")

if __name__ == "__main__":
    main()

