import openai
import logging
import json
import os

logging.basicConfig(level=logging.INFO)

class ChatGPTClient:
    def __init__(self, config_file):
        logging.info("Initializing ChatGPTClient")
        self.api_key = self.load_api_key(config_file)
        openai.api_key = self.api_key

    def load_api_key(self, config_file):
        logging.info(f"Loading API key from {config_file}")
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                config = json.load(file)
                return config.get('openai_api_key')
        else:
            logging.error(f"Config file {config_file} not found")
            return None

    def send_message(self, message):
        logging.info(f"Sending message to ChatGPT")
        try:
            prompt = "the following is a wikipedia article. Turn the info in the article into a 60 second script for a narration\n" + message
            with open("prompt.txt", "w") as file:
                file.write(prompt)
            logging.info("Prompt written to prompt.txt")
            response = input("Please enter the response from ChatGPT: ")
            with open("prompt.txt", "w") as file:
                file.write(response.strip())
            return response.strip()
        except Exception as e:
            logging.error(f"Failed to send message to ChatGPT: {e}")
            return "Failed to send message to ChatGPT"

if __name__ == "__main__":
    config_file = "config.json"
    client = ChatGPTClient(config_file)
    response = client.send_message("Hello, ChatGPT!")
    print("ChatGPT Response:")
    print(response)
