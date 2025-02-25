from gtts import gTTS
import os
import logging
from wiki import WikipediaArticle

logging.basicConfig(level=logging.INFO)

def narrate_article():
    logging.info("Starting narration of Wikipedia article")
    article = WikipediaArticle()
    if article.article_title:
        logging.info(f"Retrieved article title: {article.article_title}")
        article_text = article.get_random_wikipedia_article_text()
        tts = gTTS(text=article_text, lang='en')
        tts.save("article.mp3")
        logging.info("Saved article text to article.mp3")
    else:
        logging.error("Failed to retrieve article title")
        print("Failed to retrieve article title")

if __name__ == "__main__":
    narrate_article()
