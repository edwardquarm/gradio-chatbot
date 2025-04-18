import gradio as gr
import time
import os
import requests
import truststore
import httpx
import json

truststore.inject_into_ssl()

MODEL_API = os.getenv("MODEL_API")
MODEL_ID = os.getenv("MODEL_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

class Chatbot:
    def __init__(self):
        if not MODEL_API or not MODEL_ID or not ACCESS_TOKEN:
            raise ValueError("Environment variables MODEL_API, MODEL_ID, and ACCESS_TOKEN must be set.")
        self.messages = []
        gr.ChatInterface(
            fn=self.chat,
            title="Chatbot",
            description="A simple chatbot interface.",
            type="messages",
        ).launch()
        

    def chat(self, message, history):
        self.messages.append({"role": "user", "content": message})
        for partial_response in self.generate_response(message):
            yield partial_response
    
    
    def generate_response(self, message):
        url = f"{MODEL_API}/v1/chat/completions"
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        }
        data = {
            "model": MODEL_ID,
            "messages": self.messages,
            "stream": False,  # Disable streaming in the API request
        }
        try:
            # Make a POST request to get the full response
            response = httpx.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            response_json = response.json()  # Parse the response as JSON

            # Extract the content from the response
            full_content = ""
            for choice in response_json.get("choices", []):
                delta = choice.get("message", {})
                content = delta.get("content", "")
                full_content += content

            # Stream the content word by word
            words = full_content.split()
            if not words:
                yield "No response received from the model."
            for i in range(len(words)):
                time.sleep(0.1)  # Simulate delay for streaming
                yield " ".join(words[:i + 1])

        except Exception as e:
            yield f"Error occurred while generating response: {e}"