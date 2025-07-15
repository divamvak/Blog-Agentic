from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()

    def get_llm(self):
        try:
            self.groq_api_key = os.getenv("GROQ_API_KEY")
            print(f"GROQ_API_KEY: {self.groq_api_key}")
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            llm = ChatGroq(api_key=self.groq_api_key, model="llama-3.1-8b-instant")
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")