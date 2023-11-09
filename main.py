from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json

app = FastAPI()

@app.get("/most_interesting_article")
async def most_interesting_article():
    category_url = 'https://techcrunch.com/category/artificial-intelligence/'
    articles = get_article_links(category_url)
    sentiments = {}

    for article_url in articles:
        title, content = get_article_details(article_url)
        sentiment = analyze_sentiment(content)
        sentiments[article_url] = (sentiment, title, content)

    # Find the article with the best sentiment
    best_article_url = max(sentiments, key=lambda x: sentiments[x][0])
    best_article_sentiment, best_article_title, best_article_content = sentiments[best_article_url]

    # Construct a JSON object to return
    best_article_data = {
        "title": best_article_title,
        "content": best_article_content
    }

    return best_article_data

def get_article_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # The selector may need to be updated based on the website's structure
    links = [a['href'] for a in soup.select('a.post-block__title__link')[:2]]
    return links

def get_article_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # The selector for title may need to be updated based on the website's structure
    title = soup.select_one('h1.article__title').get_text(strip=True)
    # The selector for content may need to be updated based on the website's structure
    article_text = ' '.join(p.get_text() for p in soup.select('div.article-content p'))
    return title, article_text

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity