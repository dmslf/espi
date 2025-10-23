import requests
from bs4 import BeautifulSoup
import csv
from datetime import date, timedelta

# --- PARAMETRY ---
data = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

base_url = "https://espiebi.pap.pl/wyszukiwarka"
params = {
    "created": data,
    "enddate": f"{data} 23:59",
    "page": 0
}

all_entries = []

while True:
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = soup.select("li.news")
    if not news_items:
        print(f"Brak wyników na stronie {params['page']}. Koniec.")
        break

    for li in news_items:
        godzina = ""
        numer = ""
        hours = li.select("div.hour")
        if len(hours) >= 1:
            godzina = hours[0].get_text(strip=True)
        if len(hours) >= 2:
            numer = hours[1].get_text(strip=True)

        link_tag = li.select_one("a.link")
        tytul = link_tag.get_text(strip=True) if link_tag else ""
        link = "https://espiebi.pap.pl" + link_tag["href"] if link_tag else ""

        all_entries.append([data, godzina, numer, tytul, link])

    print(f"Pobrano stronę {params['page']} ({len(news_items)} komunikatów).")
    params["page"] += 1

# --- ZAPIS DO CSV ---
filename = f"espi_{data}.csv"

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "hour", "number", "title", "link"])
    writer.writerows(all_entries)

print(f"\nZapisano {len(all_entries)} komunikatów do pliku: {filename}")
