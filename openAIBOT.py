from pocketsphinx import LiveSpeech, get_model_path
from gtts import gTTS
import subprocess
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Initialize the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.eval()

# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Customizing the output voice (not applicable for gTTS)

def get_response(user_input):
    input_ids = tokenizer.encode(user_input, return_tensors='pt').to(device)
    with torch.no_grad():
        output = model.generate(input_ids, max_length=100, num_return_sequences=1)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
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
