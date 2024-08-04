import speech_recognition as sr
import pyttsx3
import openai
import random

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'  # Replace with your actual API key

# Flashcards data
flashcards = [
    ("Products - Residential Spaces", "Greg has worked on designing residential spaces including homes, apartments, penthouses, and beach houses, using custom textiles, fabrics, rugs, and materials to add color, pattern, warmth, and an organic feel."),
    ("Products - Commercial Spaces", "Greg has designed commercial spaces like hotels, lobbies, retail stores, and restaurants, utilizing custom-made textiles, fabrics, rugs, and materials to enhance the ambiance."),
    # Add more flashcards here
]

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
    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        print(f"OpenAI API error: {e}")
        return "This is a mock response as the API key is currently disabled."

def ask_flashcard():
    flashcard = random.choice(flashcards)
    question, answer = flashcard
    tts_engine.say(question)
    tts_engine.runAndWait()
    return question, answer

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

flashcard_question = None
flashcard_answer = None

while True:
    try:
        print("Listening...")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Adjusting for ambient noise...")

            audio = recognizer.listen(source)
            print("Audio captured, processing...")

            response = recognizer.recognize_google(audio)
            print(f"Recognized: {response}")

            if "jarvis" in response.lower():
                response_from_openai = get_response(response)
                print(f"Response from OpenAI: {response_from_openai}")
                tts_engine.say(response_from_openai)
                tts_engine.runAndWait()
            elif "flashcard" in response.lower():
                flashcard_question, flashcard_answer = ask_flashcard()
                print(f"Flashcard question: {flashcard_question}")
                print(f"Flashcard answer: {flashcard_answer}")
                tts_engine.say("The answer is: " + flashcard_answer)
                tts_engine.runAndWait()
            elif flashcard_answer and response.lower().strip() in flashcard_answer.lower():
                tts_engine.say("Correct!")
                tts_engine.runAndWait()
                flashcard_question = None
                flashcard_answer = None
            else:
                print("Didn't recognize command or wrong flashcard answer.")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error: {e}")
