import requests, json
from datetime import datetime
safe_int = lambda v: int(str(v).replace(".", "").replace(",", "")) if str(v).replace(".", "").replace(",", "").isdigit() else 0
r = requests.get("https://api.subito.it/v1/ads/list?user_id=123240534&size=100", headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept": "application/json", "Referer": "https://www.subito.it/"}, timeout=30)
print("Status: " + str(r.status_code))
print(r.text[:1000])
ads = r.json().get("ads", []) if r.status_code == 200 else []
print("Annunci: " + str(len(ads)))
cars = []
for a in ads: gal=[u for u in [img.get("uri","") or (img["scale"][-1].get("uri","") if "scale" in img else "") for img in a.get("images",[])] if u]; feat={ff.get("uri","").split("/")[-1]:ff["values"][0].get("key","") for ff in a.get("features",[]) if ff.get("values")}; cars.append({"titolo":a.get("subject",""),"anno":feat.get("year",""),"km":safe_int(feat.get("mileage",0)),"carburante":feat.get("fuel_type",""),"cambio":feat.get("gear",""),"prezzo":safe_int(a.get("price",{}).get("amount",0)),"foto":gal[0] if gal else "","galleria":gal,"link":a.get("urls",{}).get("default","")})
print("Totale: " + str(len(cars)))
json.dump({"ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y alle %H:%M"), "totale_auto": len(cars), "auto": cars}, open("data/cars.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("Fine")
