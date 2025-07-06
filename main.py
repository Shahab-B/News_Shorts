from utils.fetch_article import extract_article_text
from flow_controller import run_pipeline
from validator.scene_format_checker import check_descriptor_leaks

url = "https://www.nytimes.com/2025/06/30/us/wess-roley-idaho-shooting-suspect.html"

article_text = extract_article_text(url)

if __name__ == "__main__":
    result = run_pipeline(article_text)

    print("\n--- Pipeline Output ---\n")
    print(result)

    print("\n--- Descriptor/Name Leak Check ---")
    leaks = check_descriptor_leaks(result)
    if leaks:
        for leak in leaks:
            print(f"❌ {leak}")
    else:
        print("✅ No descriptor/name leaks detected in Scene Descriptions.")
