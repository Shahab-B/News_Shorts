from utils.fetch_article import extract_article_text
from flow_controller import run_pipeline

url = "https://www.nytimes.com/2025/06/30/us/wess-roley-idaho-shooting-suspect.html"

article_text = extract_article_text(url)

if __name__ == "__main__":
    result = run_pipeline(article_text)
    print("\n--- Pipeline Output ---\n")
    print(result)
