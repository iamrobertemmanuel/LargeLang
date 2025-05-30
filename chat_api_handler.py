from utils import convert_bytes_to_base64_with_prefix, load_config, convert_bytes_to_base64
from vectordb_handler import load_vectordb
from dotenv import load_dotenv
import streamlit as st
import requests
import os
import google.generativeai as genai
import PIL.Image
import io

load_dotenv()
config = load_config()

# Configure Gemini
genai.configure(
    api_key=config["gemini"]["api_key"],
    transport="rest"
)

class GeminiChatAPIHandler:
    AVAILABLE_MODELS = [
        "gemini-2.0-flash",  # New flash model
        "gemini-pro",
        "gemini-1.0-pro",
        "gemini-pro-vision",
        "gemini-1.0-pro-vision",
        "gemini-ultra",
        "gemini-ultra-vision"
    ]

    def __init__(self):
        pass

    @classmethod
    def try_models(cls, prompt):
        """Try different models and return the first successful response"""
        for model_name in cls.AVAILABLE_MODELS:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                print(f"Success with model: {model_name}")
                return response.text
            except Exception as e:
                print(f"Error with model {model_name}: {str(e)}")
                continue
        return "All models failed. Please check your API key and permissions."

    @classmethod
    def api_call(cls, chat_history):
        try:
            # Initialize the model with the correct model name
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Prepare the conversation as a single string with clear separation
            messages = []
            for message in chat_history:
                prefix = "User: " if message["role"] == "user" else "Assistant: "
                messages.append(f"{prefix}{message['content']}")
            
            # Generate response
            prompt = "\n".join(messages)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error with gemini-2.0-flash, trying gemini-pro: {str(e)}")
            try:
                # Fallback to gemini-pro if flash fails
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Error with gemini-pro: {str(e)}")
                return f"Error: {str(e)}"

    @classmethod
    def image_chat(cls, user_input, chat_history, image):
        try:
            model = genai.GenerativeModel('gemini-pro-vision')
            img = PIL.Image.open(io.BytesIO(image))
            response = model.generate_content([user_input, img])
            return response.text
        except Exception as e:
            print(f"Error with image chat: {str(e)}")
            return f"Error: {str(e)}"

class OpenAIChatAPIHandler:
    def __init__(self):
        pass

    @classmethod
    def api_call(cls, chat_history):
        data = {
            "model": st.session_state["model_to_use"],
            "messages": chat_history,
            "stream": False
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }

        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            json=data,
            headers=headers
        )
        print(response.json())
        json_response = response.json()
        if "error" in json_response.keys():
            return json_response["error"]["message"]
        else:
            return response.json()["choices"][0]["message"]["content"]

    @classmethod
    def image_chat(cls, user_input, chat_history, image):
        chat_history.append({
            "role": "user",
            "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {"url": convert_bytes_to_base64_with_prefix(image)}}
            ]
        })
        return cls.api_call(chat_history)

class ChatAPIHandler:
    def __init__(self):
        pass

    @classmethod
    def chat(cls, user_input, chat_history, image=None):
        endpoint = st.session_state["endpoint_to_use"]
        print(f"Endpoint to use: {endpoint}")
        print(f"Model to use: {st.session_state['model_to_use']}")
        
        if endpoint == "openai":
            handler = OpenAIChatAPIHandler
        elif endpoint == "gemini":
            handler = GeminiChatAPIHandler
        else:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        if st.session_state.get("pdf_chat", False):
            vector_db = load_vectordb()
            retrieved_documents = vector_db.similarity_search(user_input, k=st.session_state.retrieved_documents)
            context = "\n".join([item.page_content for item in retrieved_documents])
            template = f"Answer the user question based on this context: {context}\nUser Question: {user_input}"
            chat_history.append({"role": "user", "content": template})
            return handler.api_call(chat_history)
        
        if image:
            return handler.image_chat(user_input, chat_history, image)
        
        chat_history.append({"role": "user", "content": user_input})
        return handler.api_call(chat_history)