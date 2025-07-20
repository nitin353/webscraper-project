import requests
from bs4 import BeautifulSoup
import re
import random
import time

def get_tech_stack(html_text):
    tech_keywords = ["React", "Angular", "Vue", "Node.js", "Django", "Flask", "AWS", "Azure", "Firebase"]
    return [tech for tech in tech_keywords if tech.lower() in html_text.lower()]

def scrape_company_info(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')

        data = {
            "company_name": soup.title.string.strip() if soup.title else "N/A",
            "website": url,
            "emails": list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.text))),
            "phone_numbers": list(set(re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', res.text))),
            "tech_stack": get_tech_stack(res.text)
        }

        # Add a small delay to avoid hitting too many servers too quickly
        time.sleep(random.uniform(2, 4))

        return data

    except Exception as e:
        return {
            "website": url,
            "error": str(e)
        }
