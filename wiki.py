import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class WikipediaArticle:
    def __init__(self):
        logging.info("Initializing WikipediaArticle")
        self.article_title = self.get_random_wikipedia_article_title()

    def get_random_wikipedia_article_summary(self):
        logging.info(f"Fetching summary for article: {self.article_title}")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{self.article_title}"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
            return data.get('extract', 'No summary available')
        else:
            logging.error("Failed to retrieve article summary")
            return "Failed to retrieve article summary"

    def get_random_wikipedia_article_text(self):
        logging.info(f"Fetching text for article: {self.article_title}")
        url = f"https://en.wikipedia.org/api/rest_v1/page/html/{self.article_title}"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            logging.error("Failed to retrieve article text")
            return "Failed to retrieve article text"

    def get_random_wikipedia_article_title(self):
        logging.info("Fetching a random Wikipedia article title")
        url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
            return data.get('title', None)
        else:
            logging.error("Failed to retrieve article title")
            return None

    def get_article_popularity(self):
        logging.info(f"Fetching popularity for article: {self.article_title}")
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&titles={self.article_title}&format=json"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
            pages = data.get('query', {}).get('pages', {})
            page_id = next(iter(pages))
            pageviews = pages[page_id].get('pageviews', {})
            total_views = sum(view for view in pageviews.values() if view)
            return total_views
        else:
            logging.error("Failed to retrieve article popularity")
            return "Failed to retrieve article popularity"

if __name__ == "__main__":
    article = WikipediaArticle()
    if article.article_title:
        logging.info(f"Retrieved article title: {article.article_title}")
        article_summary = article.get_random_wikipedia_article_summary()
        print("Article Summary:")
        print(article_summary)
        
        article_text = article.get_random_wikipedia_article_text()
        print("\nArticle Text:")
        print(article_text)
        
        article_popularity = article.get_article_popularity()
        print("\nArticle Popularity:")
        print(article_popularity)
    else:
        logging.error("Failed to retrieve article title")
        print("Failed to retrieve article title")
