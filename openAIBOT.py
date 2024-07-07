from pocketsphinx import LiveSpeech, get_model_path
from gtts import gTTS
import subprocess
import openai

# Set your OpenAI API key and customize the chatgpt role
openai.api_key = "xyz"
messages = [{"role": "system", "content": "Your name is Jarvis and give answers in 2 lines"}]

# Customizing the output voice (not applicable for gTTS)

def get_response(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

# Initialize PocketSphinx recognizer
MODELDIR = get_model_path()
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(MODELDIR, 'en-us'),
    lm=os.path.join(MODELDIR, 'en-us.lm.bin'),
    dic=os.path.join(MODELDIR, 'cmudict-en-us.dict')
)

while True:
    try:
        print("Listening...")
        for phrase in speech:
            response = str(phrase)
            print(f"Recognized: {response}")

            if "jarvis" in response.lower():
                response_from_openai = get_response(response)
                tts = gTTS(text=response_from_openai, lang='en')
                tts.save("/tmp/output.mp3")  # Save to a temporary file
                subprocess.run(["mpg321", "/tmp/output.mp3"])
                break
            else:
                print("Didn't recognize 'jarvis'.")

    except Exception as e:
        print(f"Error: {e}")
