from pocketsphinx import LiveSpeech, get_model_path
from gtts import gTTS
import subprocess
import gpt_2_simple as gpt2

# Download the GPT-2 model (if not already downloaded)
gpt2.download_gpt2(model_name="124M")

# Customizing the output voice (not applicable for gTTS)

def get_response(user_input):
    response = gpt2.generate(sess, prefix=user_input, return_as_list=True)[0]
    return response

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

# Start a TensorFlow session for GPT-2
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, model_name="124M")

while True:
    try:
        print("Listening...")
        for phrase in speech:
            response = str(phrase)
            print(f"Recognized: {response}")

            if "jarvis" in response.lower():
                response_from_gpt = get_response(response)
                tts = gTTS(text=response_from_gpt, lang='en')
                tts.save("/tmp/output.mp3")  # Save to a temporary file
                subprocess.run(["mpg321", "/tmp/output.mp3"])
                break
            else:
                print("Didn't recognize 'jarvis'.")

    except Exception as e:
        print(f"Error: {e}")
