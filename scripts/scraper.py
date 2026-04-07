import requests, json, re, os
from datetime import datetime

USER_ID = "123240534"
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept-Language": "it-IT,it;q=0.9"}

print("=== INIZIO SCRAPER ===")
url = "https://www.subito.it/utente/" + USER_ID
print("Fetching: " + url)
r = requests.get(url, headers=H)
print("Status: " + str(r.status_code))
print("Lunghezza pagina: " + str(len(r.text)))

# Salva pagina per debug
print("Primi 500 caratteri:")
print(r.text[:500])
print("---")

# Cerca NEXT_DATA
m = re.search(r"__NEXT_DATA__[^>]*>(.*?)</script>", r.text, re.DOTALL)
if m:
    print("NEXT_DATA trovato!")
    data = json.loads(m.group(1))
    print("Chiavi principali: " + str(list(data.keys())))
    if "props" in data:
        print("Props chiavi: " + str(list(data["props"].keys())))
        if "pageProps" in data["props"]:
            pp = data["props"]["pageProps"]
            print("PageProps chiavi: " + str(list(pp.keys())))
            print("PageProps dump (primi 2000 char): " + json.dumps(pp, ensure_ascii=False)[:2000])
else:
    print("NEXT_DATA NON trovato")
    # Cerca altri pattern
    patterns = ["window.__data", "window.__PRELOADED_STATE", "application/ld+json", "itemListElement"]
    for p in patterns:
        if p in r.text:
            print("Trovato pattern: " + p)
        else:
            print("NON trovato: " + p)

print("=== FINE SCRAPER ===")
