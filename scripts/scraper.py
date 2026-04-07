import requests, json
from datetime import datetime

USER_ID = "123240534"

print("=== Scarico da API Subito ===")

H = {
"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
"Accept": "application/json",
"Accept-Language": "it-IT,it;q=0.9",
"Referer": "https://www.subito.it/"
}

url = "https://api.subito.it/v1/ads/list?user_id=" + USER_ID + "&size=100&category_id=31"
print("URL: " + url)

r = requests.get(url, headers=H, timeout=30)
print("Status: " + str(r.status_code))
print(r.text[:1000])

cars = []

if r.status_code == 200:
data = r.json()
ads = data.get("ads", [])
print("Annunci trovati: " + str(len(ads)))

for a in ads:
    imgs = a.get("images", [])
    foto = ""
    gal = []
    for img in imgs:
        u = img.get("uri", "")
        if not u and "scale" in img:
            u = img["scale"][-1].get("uri", "")
        if u:
            gal.append(u)
            if not foto:
                foto = u

    feat = {}
    for ff in a.get("features", []):
        if ff.get("values"):
            feat[ff.get("uri", "").split("/")[-1]] = ff["values"][0].get("key", "")

    p = 0
    try:
        p = int(a.get("price", {}).get("amount", 0))
    except Exception:
        pass

    km = 0
    try:
        km = int(str(feat.get("mileage", "0")).replace(".", ""))
    except Exception:
        pass

    cars.append({
        "titolo": a.get("subject", ""),
        "anno": feat.get("year", ""),
        "km": km,
        "carburante": feat.get("fuel_type", ""),
        "cambio": feat.get("gear", ""),
        "prezzo": p,
        "foto": foto,
        "galleria": gal,
        "link": a.get("urls", {}).get("default", "")
    })
    print("+ " + cars[-1]["titolo"])

else:
print("API bloccata, status: " + str(r.status_code))

with open("data/cars.json", "w", encoding="utf-8") as f:
json.dump({
    "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y alle %H:%M"),
    "totale_auto": len(cars),
    "auto": cars
}, f, ensure_ascii=False, indent=2)

print("Fine. Totale auto: " + str(len(cars)))
