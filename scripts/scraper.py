import requests
import json
import re
import os
from datetime import datetime

USER_ID = "123240534"

HEADERS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
"Accept-Language": "it-IT,it;q=0.9",
}

def fetch_subito():
print("Fetching annunci Subito.it...")
url = "https://www.subito.it/hades/v1/search/ads"
params = {
    "user_id": USER_ID,
    "lim": 50,
    "sort_by": "datedesc"
}
response = requests.get(url, params=params, headers=HEADERS)
if response.status_code != 200:
    print("Hades API fallita, provo pagina web...")
    return fetch_from_page()
data = response.json()
return parse_ads(data.get("ads", []))

def fetch_from_page():
url = "https://www.subito.it/utente/" + USER_ID
response = requests.get(url, headers=HEADERS)
if response.status_code != 200:
    print("Errore: " + str(response.status_code))
    return []
match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', response.text, re.DOTALL)
if not match:
    print("Dati non trovati nella pagina")
    return []
data = json.loads(match.group(1))
try:
    ads = data["props"]["pageProps"]["ads"]
    return parse_ads(ads)
except (KeyError, TypeError) as e:
    print("Struttura dati diversa: " + str(e))
    try:
        items = data["props"]["pageProps"]["initialState"]["items"]["list"]
        return parse_ads(items)
    except (KeyError, TypeError):
        print("Impossibile trovare annunci")
        return []

def parse_ads(ads):
print("Trovati " + str(len(ads)) + " annunci")
cars = []
for item in ads:
    try:
        features = {}
        for f in item.get("features", []):
            key = f.get("uri", "").split("/")[-1] if "/" in f.get("uri", "") else f.get("label", "")
            vals = f.get("values", [])
            if vals:
                features[key] = vals[0].get("value", vals[0].get("key", ""))
        images = item.get("images", [])
        foto = ""
        galleria = []
        for img in images:
            img_url = ""
            if "scale" in img:
                scales = img["scale"]
                if scales:
                    img_url = scales[-1].get("uri", scales[-1].get("secureuri", ""))
            elif "uri" in img:
                img_url = img["uri"]
            elif "cdnBaseUrl" in img:
                img_url = img["cdnBaseUrl"]
            if img_url:
                galleria.append(img_url)
                if not foto:
                    foto = img_url
        subject = item.get("subject", item.get("title", ""))
        price_data = item.get("features", [])
        price = 0
        for f in price_data:
            if "price" in f.get("uri", "").lower() or f.get("label", "").lower() == "prezzo":
                vals = f.get("values", [])
                if vals:
                    try:
                        price = int(str(vals[0].get("value", "0")).replace(".", "").replace(",", ""))
                    except ValueError:
                        price = 0
        if price == 0:
            try:
                price = int(item.get("price", {}).get("amount", 0))
            except (ValueError, TypeError, AttributeError):
                pass
        if price == 0:
            try:
                price = int(item.get("prices", {}).get("value", {}).get("amount", 0))
            except (ValueError, TypeError, AttributeError):
                pass
        link = item.get("urls", {}).get("default", "")
        if not link:
            link = item.get("url", "")
        if not link:
            urn = item.get("urn", "")
            if urn:
                link = "https://www.subito.it/" + str(urn)
        car = {
            "id": str(item.get("urn", item.get("id", ""))),
            "titolo": subject,
            "anno": features.get("year", features.get("anno", "")),
            "km": features.get("mileage", features.get("km", 0)),
            "carburante": features.get("fuel_type", features.get("carburante", "")),
            "cambio": features.get("gear", features.get("cambio", "")),
            "prezzo": price,
            "foto": foto,
            "galleria": galleria,
            "link": link,
        }
        try:
            car["km"] = int(str(car["km"]).replace(".", "").replace(",", ""))
        except ValueError:
            car["km"] = 0
        cars.append(car)
    except Exception as e:
        print("Errore su annuncio: " + str(e))
        continue
return cars

def salva_json(cars):
os.makedirs("data", exist_ok=True)
output = {
    "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y alle %H:%M"),
    "totale_auto": len(cars),
    "auto": cars
}
with open("data/cars.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("Salvate " + str(len(cars)) + " auto in data/cars.json")

if __name__ == "__main__":
cars = fetch_subito()
if cars:
    salva_json(cars)
else:
    print("Nessuna auto trovata")
