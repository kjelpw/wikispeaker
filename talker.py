from gtts import gTTS
import os
import logging
import time
from mutagen.mp3 import MP3
from wiki import WikipediaArticle
from chatgpt_client import ChatGPTClient

logging.basicConfig(level=logging.INFO)

def narrate_article():
    logging.info("Starting narration of Wikipedia article")
    article = WikipediaArticle()
    if article.article_title:
        logging.info(f"Retrieved article title: {article.article_title}")
        article_text = article.get_random_wikipedia_article_text()
        
        logging.info("Generating narration script using ChatGPT")
        config_file = "config.json"
        chatgpt_client = ChatGPTClient(config_file)
        narration_script = chatgpt_client.send_message(article_text)
        
        while True:
            logging.info("Start tts")
            tts = gTTS(text=narration_script, lang='en')
            tts.save("article.mp3")
            logging.info("Saved article text to article.mp3")
            
            audio = MP3("article.mp3")
            if audio.info.length > 180:  # 3 minutes
                logging.info("Article narration is too long, updating prompt for a shorter script")
                with open("prompt.txt", "a") as file:
                    file.write("\n\nRemove some lines from this narration script to bring it below 3 minutes in length.")
                narration_script = chatgpt_client.send_message(article_text)
            else:
                logging.info("Article narration is within the acceptable length")
                break
    else:
        logging.error("Failed to retrieve article title")

if __name__ == "__main__":
    narrate_article()
