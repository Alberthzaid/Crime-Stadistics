import pandas as pd
import requests
import json

API_KEY = ""
MODEL = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def generate_comparative_analysis(df1: pd.DataFrame, df2: pd.DataFrame, area1: str, area2: str, question: str) -> str:
    if df1.empty or df2.empty:
        return "Not enough data to generate a comparative analysis."

    days1 = df1["DayOfWeek"].mode().tolist()
    days2 = df2["DayOfWeek"].mode().tolist()
    
    categories1 = df1["Category"].value_counts().head(3).index.tolist()
    categories2 = df2["Category"].value_counts().head(3).index.tolist()

    prompt = f"""
As a public safety analyst, compare crime trends between two areas of San Francisco:

Area A: {area1}
- Total incidents: {len(df1)}
- Most active days: {', '.join(days1)}
- Most common crimes: {', '.join(categories1)}

Area B: {area2}
- Total incidents: {len(df2)}
- Most active days: {', '.join(days2)}
- Most common crimes: {', '.join(categories2)}

User question: {question}

Here's a sample of incidents by area:

Sample from Area A:
{df1[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(5).to_csv(index=False)}

Sample from Area B:
{df2[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(5).to_csv(index=False)}

Provide:

1. Brief comparison of patterns (max 3 lines).
2. Recommendation for city authorities (max 2 lines).
3. Advice for citizens (1 line).
4. Final summary phrase.

The response must be in English and strictly in .txt format without markdown or code blocks.
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()
    except Exception as e:
        return f"❌ Error generating analysis with Gemini: {str(e)}"