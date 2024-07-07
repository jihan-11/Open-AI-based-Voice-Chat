from pocketsphinx import LiveSpeech
from gtts import gTTS
import subprocess
import os
import openai

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

# Function to fetch response from OpenAI
def get_response(user_input):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_input,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error fetching response from OpenAI: {e}")
        return "I'm sorry, there was an error processing your request."

# Initialize PocketSphinx recognizer with explicit paths
MODELDIR = '/home/jihan11/Open-AI-based-Voice-Chat-Raspberry-Pi/myenv/lib/python3.11/site-packages/pocketsphinx/model/en-us'
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
            user_input = str(phrase)
            print(f"Recognized: {user_input}")
            
            # Fetch response from OpenAI
            response_from_openai = get_response(user_input)
            print(f"Response from OpenAI: {response_from_openai}")
            
            # Convert response to speech and play it
            tts = gTTS(text=response_from_openai, lang='en')
            tts.save("/tmp/output.mp3")  # Save to a temporary file
            subprocess.run(["mpg321", "/tmp/output.mp3"])
            
            break  # Exit the for loop after processing one command

    except Exception as e:
        print(f"Error: {e}")
