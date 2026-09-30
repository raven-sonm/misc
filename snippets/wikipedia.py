# 🤖 DISCLAIMER: This code was output from CoPilot AI during a use case of trying to return all law enforcement agencies in New Mexico for a mapping task
# This code is retained and uploaded for tracking purposes

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def clean_bullet_text(text):
    """
    Remove Wikipedia-style reference tags like [1], [citation needed], etc.
    """
    # Remove anything in square brackets, including numbers and words
    return re.sub(r"\[.*?\]", "", text).strip()

def get_wikipedia_bullets(url):
  '''
  Returns dataframe of all bullet points found on a Wikipedia page.

  7.2.2026 Use Case: Return all law enforcement agencies in New Mexico to match against user inputs.
  '''
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return pd.DataFrame(columns=["wiki_bullet_points"])

    soup = BeautifulSoup(response.text, "html.parser")

    bullets = []
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li", recursive=False):
            text = li.get_text(strip=True)
            if text:
                cleaned = clean_bullet_text(text)
                if cleaned:  # Avoid empty strings after cleaning
                    bullets.append(cleaned)

    return pd.DataFrame(bullets, columns=["wiki_bullet_points"])

if __name__ == "__main__":
    wiki_url = "https://en.wikipedia.org/wiki/List_of_law_enforcement_agencies_in_New_Mexico"
    df_bullets = get_wikipedia_bullets(wiki_url)

    print(df_bullets.head(10))
    df_bullets.to_csv("wikipedia_bullets.csv", index=False)
    print("Saved cleaned bullet points to CSV file in local path.")
