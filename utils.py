import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def configure_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely fetch API key from environment variables
    return "gpt-4o"  # Ensure the model name is correct

def enable_chat_history(func):
    def wrapper(*args, **kwargs):
        # Custom logic for chat history can be added here
        return func(*args, **kwargs)
    return wrapper
