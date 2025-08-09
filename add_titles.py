import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


df = pd.read_csv("scored_events_enhanced.csv")


titles = []


for url in tqdm(df["url"]):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        
        title_tag = (
            soup.find("h1") or 
            soup.find("title") or 
            soup.find("meta", property="og:title")
        )

        if hasattr(title_tag, "text"):
            titles.append(title_tag.text.strip())
        elif hasattr(title_tag, "get"):
            titles.append(title_tag.get("content", ""))
        else:
            titles.append("")
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        titles.append("")


df["title"] = titles


df.to_csv("scored_events_enhanced_with_titles.csv", index=False)
print("✅ Titles added and saved to scored_events_enhanced_with_titles.csv")
