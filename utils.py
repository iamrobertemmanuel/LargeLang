from datetime import datetime
import base64
import yaml
import requests
from dotenv import load_dotenv
import streamlit as st
import os
import time
import google.generativeai as genai

load_dotenv()

def load_config(file_path = "config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
    
config = load_config()
genai.configure(api_key=config["gemini"]["api_key"])

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result
    return wrapper

def command(user_input):
    if user_input == "/help":
        return """Available commands:
- /help: Show this help message
- /models: List available models"""
    elif user_input == "/models":
        return list_available_models()
    else:    
        return "Invalid command. Type /help for available commands."

def list_openai_models():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    response = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {openai_api_key}"}).json()
    if response.get("error", False):
        st.warning("OpenAI Error: " + response["error"]["message"])
        return []
    else:
        return [item["id"] for item in response["data"]]

def list_gemini_models():
    try:
        models = [
            config["gemini"]["model"],  # Text model
            config["gemini"]["vision_model"]  # Vision model
        ]
        return models
    except Exception as e:
        st.warning(f"Error listing Gemini models: {str(e)}")
        return []

def list_available_models():
    models = {
        "gemini": list_gemini_models(),
        "openai": list_openai_models() if os.getenv("OPENAI_API_KEY") else []
    }
    return models
    
def convert_bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")
    
def convert_bytes_to_base64_with_prefix(image_bytes):
    return "data:image/jpeg;base64," + convert_bytes_to_base64(image_bytes)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_avatar(sender_type):
    if sender_type == "user":
        return "chat_icons/user_image.png"
    else:
       return "chat_icons/bot_image.png"

def save_config(config):
    with open("config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)