import csv
import asyncio
from playwright.async_api import async_playwright

async def scrape_comedybar_slider():
    url = "https://comedybar.ca"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_selector('.show-thumbnail-container')  

        
        containers = await page.query_selector_all('.show-thumbnail-container')

        events = []
        for i, container in enumerate(containers):
            try:
                text = await container.inner_text()
                img = await container.query_selector('img')
                img_url = await img.get_attribute('src') if img else "No image"

                
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                title = lines[0] if lines else "Untitled"
                performers = ', '.join(lines[-3:]) if len(lines) >= 3 else "Unknown"
                date_line = [l for l in lines if any(month in l.lower() for month in ["august", "september", "july"])]
                date = date_line[0] if date_line else "Unknown"
                time_line = [l for l in lines if "pm" in l.lower()]
                time = time_line[0] if time_line else "Unknown"

                events.append({
                    "title": title,
                    "date": date,
                    "time": time,
                    "performers": performers,
                    "image_url": img_url
                })

            except Exception as e:
                print(f"Error in card {i}: {e}")

        
        keys = ["title", "date", "time", "performers", "image_url"]
        with open("events_slider.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(events)

        print(f"\n✅ Saved {len(events)} events to events_slider.csv")
        await browser.close()


asyncio.run(scrape_comedybar_slider())
