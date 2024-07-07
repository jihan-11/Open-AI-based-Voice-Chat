from pocketsphinx import LiveSpeech, get_model_path
from gtts import gTTS
import subprocess
import os
import openai

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

# Customizing the output voice (not applicable for gTTS)

def get_response(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

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
