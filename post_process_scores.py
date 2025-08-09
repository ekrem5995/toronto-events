import pandas as pd

INPUT_FILE = "scored_events.csv"
OUTPUT_FILE = "scored_events_enhanced.csv"

df = pd.read_csv(INPUT_FILE)

def calculate_total(row):
    total = 0
    count = 0
    for key in ["Participatory", "Quirky", "DatingFunVibe", "KidFriendly"]:
        value = row.get(key)
        if pd.notna(value):
            try:
                total += float(value)
                count += 1
            except:
                pass
    return total if count > 0 else None

# Calculate TotalScore
df["TotalScore"] = df.apply(calculate_total, axis=1)

# Add empty Tag and PickForNewsletter columns if not already present
if "Tag" not in df.columns:
    df["Tag"] = ""

if "PickForNewsletter" not in df.columns:
    df["PickForNewsletter"] = ""

df.to_csv(OUTPUT_FILE, index=False)
print(f"Done. File saved as {OUTPUT_FILE}")
