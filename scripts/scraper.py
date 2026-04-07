import requests, json, re, os
from datetime import datetime

USER_ID = "123240534"
H = {"User-Agent": "Mozilla/5.0"}

def fetch():
    r = requests.get("https://www.subito.it/hades/v1/search/ads", params={"user_id": USER_ID, "lim": 50}, headers=H)
    if r.status_code == 200:
        return r.json().get("ads", [])
    r = requests.get("https://www.subito.it/utente/" + USER_ID, headers=H)
    if r.status_code != 200:
        return []
    m = re.search(r"__NEXT_DATA__[^>]*>(.*?)</script>", r.text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))["props"]["pageProps"]["ads"]
        except Exception:
            return []
    return []

ads = fetch()
cars = []
for a in ads:
    try:
        imgs = a.get("images", [])
        foto = imgs[0]["scale"][-1]["uri"] if imgs else ""
        gal = [i["scale"][-1]["uri"] for i in imgs if "scale" in i]
        p = 0
        try:
            p = int(a.get("price", {}).get("amount", 0))
        except Exception:
            pass
        feat = {}
        for ff in a.get("features", []):
            if ff.get("values"):
                feat[ff["uri"].split("/")[-1]] = ff["values"][0].get("key", "")
        cars.append({"titolo": a.get("subject", ""), "anno": feat.get("year", ""), "km": int(str(feat.get("mileage", "0")).replace(".", "").replace(",", "")), "carburante": feat.get("fuel_type", ""), "cambio": feat.get("gear", ""), "prezzo": p, "foto": foto, "galleria": gal, "link": a.get("urls", {}).get("default", "")})
    except Exception:
        pass

os.makedirs("data", exist_ok=True)
json.dump({"ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M"), "totale_auto": len(cars), "auto": cars}, open("data/cars.json", "w"), ensure_ascii=False, indent=2)
print("Salvate " + str(len(cars)) + " auto")
