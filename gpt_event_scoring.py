import openai
import pandas as pd
import time
import json

client = openai.OpenAI(api_key="get_your_api_key_here")

INPUT_FILE = "all_events_for_scoring.csv"
OUTPUT_FILE = "scored_events.csv"

def score_event(title, description):
    prompt = f"""
You are an AI assistant that scores public events based on their description.
Rate the following event from 1 to 10 on these dimensions:

- Participatory
- Quirky
- Dating/Fun Vibe
- Kid-friendly

Output the result as a JSON dictionary **in this exact format**:

{{
  "Participatory": 7,
  "Quirky": 8,
  "DatingFunVibe": 6,
  "KidFriendly": 5
}}

Event Title: {title}
Event Description:
{description}

JSON:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        text = response.choices[0].message.content.strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error scoring '{title}':", e)
        return {}

def normalize_keys(score_dict):
    """
    Normalize GPT's output keys to match our desired format.
    """
    normalized = {}
    for key, value in score_dict.items():
        clean_key = key.lower().replace(" ", "").replace("-", "").replace("/", "")
        normalized[clean_key] = value
    return {
        "Participatory": normalized.get("participatory"),
        "Quirky": normalized.get("quirky"),
        "DatingFunVibe": normalized.get("datingfunvibe"),
        "KidFriendly": normalized.get("kidfriendly"),
    }


df = pd.read_csv(INPUT_FILE)
results = []


for index, row in df.iterrows():
    
    title = row.get("title")
    if pd.isna(title) or not isinstance(title, str):
        title = str(title) if not pd.isna(title) else "Untitled"
    else:
        title = title.strip()

    
    desc_raw = row.get("description") or row.get("raw_text") or ""
    if pd.isna(desc_raw):
        desc_raw = ""
    description = str(desc_raw).strip()

    if len(description) < 20:
        print("Skipping:", title)
        continue

    print("Scoring:", title[:50], "...")

    scores_raw = score_event(title, description)
    scores = normalize_keys(scores_raw)

    row_data = {
        "title": title,
        "venue": str(row.get('venue', '')),
        "description": description,
        "url": str(row.get('url', '')),
        "Participatory": scores.get("Participatory"),
        "Quirky": scores.get("Quirky"),
        "DatingFunVibe": scores.get("DatingFunVibe"),
        "KidFriendly": scores.get("KidFriendly"),
    }

    results.append(row_data)
    time.sleep(1.5)


pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
print(f"Done. Results saved to {OUTPUT_FILE}")
