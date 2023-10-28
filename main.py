from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from textblob import TextBlob
import time
import json

app = FastAPI()

@app.get("/most_interesting_article")
async def most_interesting_article():
    url = "https://techcrunch.com/category/artificial-intelligence/"

    # Sending HTTP request
    reqs = requests.get(url)

    # Parsing the HTML
    soup = BeautifulSoup(reqs.text, 'html.parser')

    # Finding the articles by their HTML tag and class name
    articles = soup.find_all('a', class_='post-block__title__link', limit=3)

    # Dictionary to store article information and sentiment
    article_info = {}

    for i, article in enumerate(articles, start=1):
        # Extracting the URL of the article
        article_url = article.get('href')

        # Using newspaper3k to extract information
        article = Article(article_url)
        article.download()
        article.parse()

        # Delay for a moment to avoid sending too many requests in a short time
        time.sleep(2)

        # Analyzing sentiment
        analysis = TextBlob(article.text)
        sentiment_polarity = analysis.sentiment.polarity

        # Storing information
        article_info[i] = {
            "title": article.title,
            "url": article_url,
            "content": article.text,
            "sentiment": sentiment_polarity
        }

    # Finding the article with the highest sentiment polarity
    most_interesting_article = max(article_info.items(), key=lambda x: x[1]['sentiment'])

    # Returning the information as JSON
    return most_interesting_article[1]

