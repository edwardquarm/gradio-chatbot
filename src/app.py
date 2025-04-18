import gradio as gr
import time


class Chatbot:
    def __init__(self):
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
        # stream response
        words = message.split()
        for i in range(len(words)):
            time.sleep(0.1)
            yield " ".join(words[:i + 1])