let tutteLeAuto = [];
let fotoCorrente = 0;
let fotoAttuale = [];

// ── CARICA AUTO ──
async function init() {
try {
  const res = await fetch("data/cars.json");
  const data = await res.json();
  tutteLeAuto = data.auto;
  document.getElementById("info-update").textContent =
    `✅ ${data.totale_auto} auto disponibili · Aggiornato ${data.ultimo_aggiornamento}`;
  mostraAuto(tutteLeAuto);
} catch {
  console.log("JSON non trovato, uso dati di test");
  tutteLeAuto = datiTest();
  mostraAuto(tutteLeAuto);
}
}

// ── MOSTRA AUTO ──
function mostraAuto(auto) {
const grid = document.getElementById("car-grid");

if (!auto.length) {
  grid.innerHTML = `
    <p style="color:#666; grid-column:1/-1; text-align:center; padding:40px">
      Nessuna auto disponibile al momento.
    </p>`;
  return;
}

grid.innerHTML = auto.map((car, i) => `
  <div class="car-card" onclick="apriPopup(${i})">
    <img
      src="${car.foto || 'img/placeholder.jpg'}"
      alt="${car.titolo}"
      loading="lazy"
      onerror="this.src='https://via.placeholder.com/400x200/111/333?text=GRS+Cars'"
    >
    <div class="car-body">
      <h3>${car.titolo}</h3>
      <p class="dettagli">
        ${[
          car.anno,
          car.km ? car.km.toLocaleString('it') + ' km' : '',
          car.carburante,
          car.cambio
        ].filter(Boolean).join(' | ')}
      </p>
      <p class="prezzo">
        ${car.prezzo ? '€ ' + car.prezzo.toLocaleString('it') : 'Su richiesta'}
      </p>
      <span class="btn-annuncio">VAI ALL'ANNUNCIO</span>
    </div>
  </div>
`).join("");
}

// ── APRI POPUP ──
function apriPopup(index) {
const car = tutteLeAuto[index];
fotoAttuale = car.galleria?.length ? car.galleria : (car.foto ? [car.foto] : []);
fotoCorrente = 0;

aggiornaFoto();

document.getElementById("popup-titolo").textContent = car.titolo;
document.getElementById("popup-dettagli").textContent =
  [
    car.anno,
    car.km ? car.km.toLocaleString('it') + ' km' : '',
    car.carburante,
    car.cambio
  ].filter(Boolean).join(" | ");

document.getElementById("popup-prezzo").textContent =
  car.prezzo ? `€ ${car.prezzo.toLocaleString('it')}` : "Prezzo su richiesta";

document.getElementById("popup-link").href = car.link || "#";

document.getElementById("popup-overlay").classList.remove("hidden");
document.body.style.overflow = "hidden";
}

// ── AGGIORNA FOTO POPUP ──
function aggiornaFoto() {
const img = document.getElementById("popup-img");
img.src = fotoAttuale[fotoCorrente]
  || 'https://via.placeholder.com/700x340/111/333?text=GRS+Cars';
document.getElementById("foto-counter").textContent =
  `📸 ${fotoCorrente + 1} / ${fotoAttuale.length}`;
}

// ── CHIUDI POPUP ──
function chiudiPopup() {
document.getElementById("popup-overlay").classList.add("hidden");
document.body.style.overflow = "";
}

// Chiudi cliccando fuori
document.getElementById("popup-overlay").onclick = (e) => {
if (e.target === document.getElementById("popup-overlay")) chiudiPopup();
};

// Bottoni freccia
document.getElementById("popup-close").onclick = chiudiPopup;

document.getElementById("prev").onclick = (e) => {
e.stopPropagation();
fotoCorrente = (fotoCorrente - 1 + fotoAttuale.length) % fotoAttuale.length;
aggiornaFoto();
};

document.getElementById("next").onclick = (e) => {
e.stopPropagation();
fotoCorrente = (fotoCorrente + 1) % fotoAttuale.length;
aggiornaFoto();
};

// Tastiera
document.addEventListener("keydown", (e) => {
if (e.key === "Escape")      chiudiPopup();
if (e.key === "ArrowLeft")   document.getElementById("prev").click();
if (e.key === "ArrowRight")  document.getElementById("next").click();
});

// ── DATI DI TEST ──
function datiTest() {
return [
  {
    titolo: "Fiat 500 1.0 Hybrid Dolcevita",
    anno: "2022", km: 18000,
    carburante: "Ibrido", cambio: "Manuale",
    prezzo: 14900,
    foto: "https://via.placeholder.com/400x200/111/c0392b?text=Fiat+500",
    galleria: [],
    link: "https://www.subito.it/utente/123240534"
  },
  {
    titolo: "Volkswagen Golf 1.6 TDI Business",
    anno: "2021", km: 45000,
    carburante: "Diesel", cambio: "Manuale",
    prezzo: 19500,
    foto: "https://via.placeholder.com/400x200/111/c0392b?text=VW+Golf",
    galleria: [],
    link: "https://www.subito.it/utente/123240534"
  },
  {
    titolo: "BMW Serie 3 318d Advantage",
    anno: "2020", km: 62000,
    carburante: "Diesel", cambio: "Automatico",
    prezzo: 24900,
    foto: "https://via.placeholder.com/400x200/111/c0392b?text=BMW+Serie+3",
    galleria: [],
    link: "https://www.subito.it/utente/123240534"
  },
  {
    titolo: "Toyota Yaris 1.5 Hybrid Active",
    anno: "2023", km: 12000,
    carburante: "Ibrido", cambio: "Automatico",
    prezzo: 19800,
    foto: "https://via.placeholder.com/400x200/111/c0392b?text=Toyota+Yaris",
    galleria: [],
    link: "https://www.subito.it/utente/123240534"
  },
  {
    titolo: "Audi A3 35 TFSI S-Line",
    anno: "2022", km: 38000,
    carburante: "Benzina", cambio: "Automatico",
    prezzo: 27400,
    foto: "https://via.placeholder.com/400x200/111/c0392b?text=Audi+A3",
    galleria: [],
    link: "https://www.subito.it/utente/123240534"
  },
  {
    titolo: "Renault Clio 1.0 TCe Zen",
    anno: "2022", km: 29000,
    carburante: "Benzina", cambio: "Manuale",
    prezzo: 14200,
    foto: "https://via.placeholder.com/400x200/111/c0392b?text=Renault+Clio",
    galleria: [],
    link: "https://www.subito.it/utente/123240534"
  }
];
}

init();