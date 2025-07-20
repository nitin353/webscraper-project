from search_scraper import get_company_urls, get_competitors
from site_scraper import scrape_company_info
import pandas as pd
import os
import json

def main():
    query = input("Enter a search query (e.g., 'AI startups in India'): ").strip()
    if not query:
        print("❌ Empty query. Please try again.")
        return

    urls = get_company_urls(query, num_results=5)
    results = []

    os.makedirs("output", exist_ok=True)

    for url in urls:
        print(f"🔍 Scraping: {url}")
        info = scrape_company_info(url)

        # Add competitors based on company name
        if "company_name" in info and info["company_name"] != "N/A":
            print(f"🔎 Searching competitors for {info['company_name']}...")
            competitors = get_competitors(info['company_name'], num_results=3)
            info["competitors"] = competitors
        else:
            info["competitors"] = []

        results.append(info)

    # Save JSON
    with open("output/companies.json", "w") as f:
        json.dump(results, f, indent=4)
    print("✅ Data saved to output/companies.json")

    # Save CSV
    df = pd.DataFrame(results)
    df.to_csv("output/companies.csv", index=False)
    print("📁 CSV saved to output/companies.csv")

if __name__ == "__main__":
    main()
