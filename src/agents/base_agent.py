from langchain_ollama import OllamaLLM  
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature=0.5, use_local=True):
    """
    Get LLM - local Ollama (free, unlimited) or Groq (rate limited)
    """
    if use_local:
        return OllamaLLM(  
            model="llama3.2",
            temperature=temperature
        )
    else:
        return ChatGroq(
            temperature=temperature,
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
