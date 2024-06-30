import speech_recognition as sr # type: ignore
import pyttsx3 # type: ignore
import openai # type: ignore

# Initialize pyttsx3
engine = pyttsx3.init()

# Set your OpenAI API key and customize the chatgpt role
openai.api_key = "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"
messages = [{"role": "system", "content": "Your name is Jarvis and give answers in 2 lines"}]

# Customizing the output voice
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response.choices[0].message['content']
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5.0)
    
    try:
        response = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        response = None
    
    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    listening = True

    while listening:
        print("Listening...")
        speech_text = recognize_speech_from_mic(recognizer, microphone)
        
        if speech_text is None:
            print("Didn't recognize anything.")
            continue
        
        print(f"Recognized: {speech_text}")
        
        if "jarvis" in speech_text.lower():
            response_from_openai = get_response(speech_text)
            engine.setProperty('rate', 120)
            engine.setProperty('volume', volume)
            engine.setProperty('voice', greek[0].id)  # Adjust as needed for specific voice
            engine.say(response_from_openai)
            engine.runAndWait()
        else:
            print("Didn't recognize 'jarvis'.")

if __name__ == "__main__":
    main()
