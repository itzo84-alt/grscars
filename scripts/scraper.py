import requests
import json
import os
from datetime import datetime

# ── CONFIGURAZIONE ──
USER_ID = "123240534"  # Il tuo ID Subito.it

HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Accept": "application/json"
}

def fetch_subito():
  print(f"🔍 Fetching annunci Subito.it utente {USER_ID}...")

  url = f"https://api.subito.it/svc/search/v1/listings?advertiser_id={USER_ID}&size=100"
  response = requests.get(url, headers=HEADERS)

  if response.status_code != 200:
      print(f"❌ Errore: status {response.status_code}")
      return []

  data = response.json()
  annunci = data.get("ads", [])
  print(f"📦 Trovati {len(annunci)} annunci")

  cars = []
  for item in annunci:
      try:
          # Features (km, anno, carburante ecc)
          features = {}
          for f in item.get("features", []):
              chiave = f.get("uri", "").split("/")[-1]
              valori = f.get("values", [])
              if valori:
                  features[chiave] = valori[0].get("key", "")

          # Foto
          immagini = item.get("images", [])
          foto_principale = ""
          tutte_foto = []

          for img in immagini:
              scale = img.get("scale", [])
              if scale:
                  uri = scale[-1].get("uri", "")
                  tutte_foto.append(uri)
                  if not foto_principale:
                      foto_principale = uri

          car = {
              "id":          str(item.get("urn", "")),
              "titolo":      item.get("subject", ""),
              "marca":       features.get("brand", ""),
              "modello":     features.get("model", ""),
              "anno":        features.get("year", ""),
              "km":          int(features.get("mileage", 0) or 0),
              "carburante":  features.get("fuel_type", ""),
              "cambio":      features.get("gear", ""),
              "potenza":     features.get("power_cv", ""),
              "colore":      features.get("colour", ""),
              "prezzo":      int(item.get("prices", {})
                                .get("value", {})
                                .get("amount", 0) or 0),
              "foto":        foto_principale,
              "galleria":    tutte_foto,
              "link":        item.get("urls", {}).get("default", ""),
              "aggiornato":  datetime.now().strftime("%d/%m/%Y %H:%M")
          }
          cars.append(car)

      except Exception as e:
          print(f"⚠️ Errore su annuncio: {e}")
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

  print(f"✅ Salvate {len(cars)} auto in data/cars.json")

if __name__ == "__main__":
  cars = fetch_subito()
  if cars:
      salva_json(cars)
  else:
      print("⚠️ Nessuna auto trovata, cars.json non aggiornato")