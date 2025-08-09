import requests
from bs4 import BeautifulSoup
import csv
import time

INPUT_CSV = "events_calendar.csv"
OUTPUT_CSV = "events_detailed.csv"

def extract_event_details(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        
        title_tag = soup.find("h1", class_="display-4")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        
        datetime_tag = soup.find("h4", class_="text-muted")
        datetime = datetime_tag.get_text(strip=True) if datetime_tag else "N/A"

        
        desc_tag = soup.find("div", class_="show-description")
        description = desc_tag.get_text(separator="\n", strip=True) if desc_tag else "N/A"

        return title, datetime, description
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "N/A", "N/A", "N/A"


with open(INPUT_CSV, newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    urls = [(row["venue"], row["link"]) for row in reader]


with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["venue", "title", "datetime", "description", "url"])

    for venue, url in urls:
        print(f"Scraping event: {url}")
        title, dt, desc = extract_event_details(url)
        writer.writerow([venue, title, dt, desc, url])
        time.sleep(1)  