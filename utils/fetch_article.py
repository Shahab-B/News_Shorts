# utils/fetch_article.py
from newspaper import Article

def extract_article_text(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    return article.text
