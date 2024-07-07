import speech_recognition as sr
from gtts import gTTS
import subprocess
import openai

# Initializing gTTS
engine = None  # Placeholder for gTTS, not needed for gTTS

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

while True:
    try:
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)

        response = recognizer.recognize_google(audio)
        print(f"Recognized: {response}")

        if "jarvis" in response.lower():
            response_from_openai = get_response(response)
            
            # Using gTTS for text-to-speech
            tts = gTTS(text=response_from_openai, lang='en')
            tts.save("/tmp/output.mp3")  # Save to a temporary file

            # Use mpg321 to play the audio
            subprocess.run(["mpg321", "/tmp/output.mp3"])
           
        else:
            print("Didn't recognize 'jarvis'.")

    except sr.UnknownValueError:
        print("Didn't recognize anything.")
    
    except sr.RequestError as e:
        print(f"Error fetching results; {e}")
    
    except Exception as e:
        print(f"Error: {e}")
