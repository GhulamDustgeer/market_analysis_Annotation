import pandas as pd
import os
import re


# 2) Load CSV
df = pd.read_csv("headline.csv")
print("Columns:", list(df.columns))
print("Rows:", len(df))

# 3) Find headline column automatically
# (pehle aisa column dhundho jiska naam headline/title/news ho)
headline_col = None
for c in df.columns:
    name = str(c).lower()
    if "headline" in name or "title" in name or "news" in name:
        headline_col = c
        break

print("Using headline column:", headline_col)


# 4) Simple labeling rules
def label_impact(text):
    t = str(text).lower()
    if re.search(r"(fall|slump|plunge|recession|downgrade|loss|crisis|layoff|miss)", t):
        return "negative"
    if re.search(r"(rise|surge|rally|record|growth|upgrade|profit|beat|strong)", t):
        return "positive"
    return "neutral"
def label_event(text):
    t = str(text).lower()
    if re.search(r"(fed|interest rate|inflation|cpi|gdp|unemployment|central bank)", t):
        return "macro"
    if re.search(r"(earnings|revenue|guidance|eps|quarter|q1|q2|q3|q4)", t):
        return "earnings"
    if re.search(r"(war|sanction|election|attack|conflict)", t):
        return "geopolitical"
    return "general"

# 5) Create new columns
df["headline_text"] = df[headline_col].astype(str)
df["impact_direction"] = df["headline_text"].apply(label_impact)
df["event_type"] = df["headline_text"].apply(label_event)

# 6) Save annotated file
BASE = r"C:\Users\Hadiii\Desktop\market_analysis_project"
out_path = os.path.join(BASE, "annotated.csv")
df[["headline_text", "event_type", "impact_direction"]].to_csv(out_path, index=False)

print("✅ Saved:", out_path)
print(df[["headline_text", "event_type", "impact_direction"]].head(5))
