# quick_test.py
from newspaper import Article

url = "https://www.bbc.com/news/world-asia-66281262"
article = Article(url)
article.download()
article.parse()
print(article.text[:500])  # just show first 500 characters
