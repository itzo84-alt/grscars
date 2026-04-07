import requests, json
from datetime import datetime

USER_ID = "123240534"
H = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept": "application/json", "Referer": "https://www.subito.it/"}
url = "https://api.subito.it/v1/ads/list?user_id=" + USER_ID + "&size=100"
r = requests.get(url, headers=H, timeout=30)
print("Status: " + str(r.status_code))
print(r.text[:1000])
data = r.json() if r.status_code == 200 else {"ads": []}
ads = data.get("ads", [])
print("Annunci trovati: " + str(len(ads)))
cars = []
for a in ads:
imgs = a.get("images", [])
foto = ""
gal = []
for img in imgs:
    u = img.get("uri", "") or (img["scale"][-1].get("uri", "") if "scale" in img else "")
    if u: gal.append(u)
    if u and not foto: foto = u
feat = {}
for ff in a.get("features", []):
    if ff.get("values"): feat[ff.get("uri", "").split("/")[-1]] = ff["values"][0].get("key", "")
p = 0
try: p = int(a.get("price", {}).get("amount", 0))
except Exception: pass
km = 0
try: km = int(str(feat.get("mileage", "0")).replace(".", ""))
except Exception: pass
cars.append({"titolo": a.get("subject", ""), "anno": feat.get("year", ""), "km": km, "carburante": feat.get("fuel_type", ""), "cambio": feat.get("gear", ""), "prezzo": p, "foto": foto, "galleria": gal, "link": a.get("urls", {}).get("default", "")})
print("+ " + cars[-1]["titolo"])
with open("data/cars.json", "w", encoding="utf-8") as f:
json.dump({"ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y alle %H:%M"), "totale_auto": len(cars), "auto": cars}, f, ensure_ascii=False, indent=2)
print("Fine. Totale: " + str(len(cars)))
