from utils.fetch_article import extract_article_text
from agents.summarizer import summarize_article
from agents.summary_refiner import polish_text
from agents.scripter import generate_script
from agents.script_refiner import polish_script

url = "https://www.bbc.com/news/newsbeat-44124396" #"https://www.nytimes.com/2025/06/30/us/wess-roley-idaho-shooting-suspect.html"  # Example
article_text = extract_article_text(url)

summary = summarize_article(article_text)
polished_summary = polish_text(summary)
script = generate_script(polished_summary)
final_script = polish_script(script)

print("\n🎯 Final Output Script:\n")
print(final_script)
