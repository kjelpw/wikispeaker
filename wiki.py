import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class WikipediaArticle:
    def __init__(self):
        logging.info("Initializing WikipediaArticle")
        self.article_title = self.get_top_5000_article_title()

    def get_random_wikipedia_article_summary(self):
        logging.info(f"Fetching summary for article: {self.article_title}")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{self.article_title}"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
            return data.get('extract', 'No summary available')
        else:
            logging.error(f"Failed to retrieve article summary: {response.status_code} - {response.text}")
            return "Failed to retrieve article summary"

    def get_random_wikipedia_article_text(self):
        logging.info(f"Fetching text for article: {self.article_title}")
        url = f"https://en.wikipedia.org/api/rest_v1/page/html/{self.article_title}"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            logging.error(f"Failed to retrieve article text: {response.status_code} - {response.text}")
            return "Failed to retrieve article text"

    def get_top_5000_article_title(self):
        logging.info("Fetching a random article title from the top 5000 list")
        url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2021/all-days"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
            articles = data.get('items', [])[0].get('articles', [])
            if articles:
                import random
                article = random.choice(articles[:5000])
                return article.get('article', None)
            else:
                logging.error("No articles found in the top 5000 list")
                return None
        else:
            logging.error(f"Failed to retrieve top 5000 articles: {response.status_code} - {response.text}")
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
            logging.error(f"Failed to retrieve article popularity: {response.status_code} - {response.text}")
            return "Failed to retrieve article popularity"

    def is_top_5000_popular(self):
        logging.info(f"Checking if article is in the top 5000 in popularity: {self.article_title}")
        url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2021/all-days"
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            data = response.json()
            articles = data.get('items', [])[0].get('articles', [])
            for article in articles[:5000]:
                if article.get('article') == self.article_title:
                    return True
            return False
        else:
            logging.error(f"Failed to retrieve top 5000 articles: {response.status_code} - {response.text}")
            return False

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
        
        is_top_5000 = article.is_top_5000_popular()
        print("\nIs Top 5000 Popular:")
        print(is_top_5000)
    else:
        logging.error("Failed to retrieve article title")
        print("Failed to retrieve article title")
