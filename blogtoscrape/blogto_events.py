from playwright.sync_api import sync_playwright
import csv
import time

INPUT_CSV = "blogto_events.csv"
OUTPUT_CSV = "blogto_detailed_raw.csv"

def extract_event_text(url, page):
    try:
        page.goto(url, timeout=30000)
        page.wait_for_timeout(3000)
        full_text = page.locator("body").inner_text()
        return full_text.strip() if full_text else "N/A"
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "N/A"

with open(INPUT_CSV, newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    events = [(row["venue"], row["title"], row["url"]) for row in reader]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["venue", "title", "raw_text", "url"])

        for venue, title, url in events:
            print(f"Scraping: {url}")
            raw_text = extract_event_text(url, page)
            writer.writerow([venue, title, raw_text, url])
            time.sleep
