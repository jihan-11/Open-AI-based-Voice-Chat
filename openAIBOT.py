import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

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

# Main function to interact with OpenAI
def main():
    try:
        user_input = "What's the weather today?"  # Example input for testing
        
        # Fetch response from OpenAI
        response_from_openai = get_response(user_input)
        print(f"Response from OpenAI: {response_from_openai}")
        
        # You can further process or output the response as needed
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
