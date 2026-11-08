// Erzeugt Teilen-Seiten und Vorschaubilder für alle Elemente mit data-teilen in index.html.
//
//   teilen/<id>.html        kleine Seite mit Open-Graph-Angaben; leitet Besucher zur Stelle in index.html
//   teilen/bilder/<id>.jpg      Vorschaubild für Linkvorschauen, 1200 × 630
//   teilen/bilder/<id>-hoch.jpg Bild für eigene Posts, 1080 × 1350
//   teilen/bilder/start.jpg     Vorschaubild der Startseite
//
// Grafiken und Kennzahlen werden als Bild der Grafik gerendert, Ereignisse als gestaltete Überschrift.
// Aufruf im Repo-Ordner:  npm install playwright  &&  npx playwright install chromium  &&  node werkzeuge/teilen.js
// Nach jeder Änderung an Zahlen, Grafiken oder Ereignissen neu ausführen.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const BASIS = 'https://kaffeeundkomiss.github.io/bundeswehr-Afghanistan-/';
const WURZEL = path.resolve(__dirname, '..');
const ZIEL = path.join(WURZEL, 'teilen');
const BILDER = path.join(ZIEL, 'bilder');
const SEITE = 'file://' + path.join(WURZEL, 'index.html');
const FORMATE = [
  { endung: '', breite: 1200, hoehe: 630, zoom: { grafik: 1.6, zahl: 1.5, ueberschrift: 1, start: 1 } },
  { endung: '-hoch', breite: 1080, hoehe: 1350, zoom: { grafik: 2.7, zahl: 2.4, ueberschrift: 1.25, start: 1.25 } }
];

const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Läuft im Browser: ersetzt die Seite durch das Teilbild eines Elements.
function rendern({ id, art, zoom, adresse }) {
  const kurz = {};
  document.querySelectorAll('.quellen li[id^="q"]').forEach((li) => {
    kurz[li.id] = li.textContent.split(':')[0].trim();
  });
  const stand = (document.querySelector('.badges span') || {}).textContent || '';
  const marke = document.querySelector('.marke').cloneNode(true);
  const box = document.createElement('div');
  box.className = 'tb tb-' + art;
  const kopf = document.createElement('div');
  kopf.className = 'tb-kopf';
  kopf.appendChild(marke);
  const inhalt = document.createElement('div');
  inhalt.className = 'tb-inhalt';
  inhalt.style.zoom = zoom;
  const fuss = document.createElement('div');
  fuss.className = 'tb-fuss';

  if (art === 'start') {
    inhalt.innerHTML = '<div class="tb-gross">Bundeswehr in Afghanistan</div><div class="tb-unter">Der Einsatz 2001–2021 in Zahlen, Daten und Quellen</div>';
    kopf.remove();
  } else if (art === 'ueberschrift') {
    const quelle = document.getElementById(id);
    const h3 = quelle.querySelector('h3');
    const zeit = h3.querySelector('time');
    const titel = Array.from(h3.childNodes).filter((n) => n !== zeit).map((n) => n.textContent).join('').trim();
    inhalt.innerHTML = '<div class="tb-datum"></div><div class="tb-gross"></div><div class="tb-unter">Was geschah, mit Quellen</div>';
    inhalt.querySelector('.tb-datum').textContent = zeit ? zeit.textContent : '';
    inhalt.querySelector('.tb-gross').textContent = titel;
  } else {
    const kopie = document.getElementById(id).cloneNode(true);
    kopie.removeAttribute('id');
    kopie.querySelectorAll('.teilen-leiste').forEach((n) => n.remove());
    // Text, der ohne den Zusammenhang der Seite verständlich ist (z. B. statt „davon …“)
    const bildtext = kopie.getAttribute('data-bildtext');
    if (bildtext && kopie.querySelector('.text')) kopie.querySelector('.text').textContent = bildtext;
    // Quellennummern sind außerhalb der Seite nicht verständlich: durch Kurznamen ersetzen
    kopie.querySelectorAll('a[href^="#q"]').forEach((a) => {
      const s = document.createElement('span');
      s.textContent = kurz[a.getAttribute('href').slice(1)] || a.textContent;
      a.replaceWith(s);
    });
    kopie.querySelectorAll('.beleg').forEach((b) => {
      b.innerHTML = b.innerHTML.replace(/<\/span>\s+<span>/g, '</span>; <span>').replace(/^(Quellen?) /, '$1: ');
    });
    inhalt.appendChild(kopie);
  }
  fuss.innerHTML = '<span></span><span></span>';
  fuss.children[0].textContent = adresse;
  fuss.children[1].textContent = stand;

  box.appendChild(kopf);
  box.appendChild(inhalt);
  box.appendChild(fuss);
  const stil = document.createElement('style');
  stil.textContent = `
    html,body{margin:0;height:100%;overflow:hidden}
    body{background:var(--head-bg) url("tarn.svg") repeat}
    .tb{position:fixed;inset:0;display:flex;flex-direction:column;gap:18px;padding:28px}
    .tb-kopf{display:flex}
    .tb-kopf .marke{padding:8px 14px 8px 10px}
    .tb-inhalt{flex:1;display:flex;flex-direction:column;justify-content:center;background:var(--paper);border:1px solid var(--braun);border-top:4px solid var(--akzent);padding:16px 22px;overflow:hidden}
    .tb-inhalt .grafik{border:0;padding:0;margin:0}
    .tb-inhalt .zahl{border:0;padding:0;background:none}
    .tb-inhalt .zahl .wert{font-size:60px;line-height:1.1}
    .tb-inhalt .zahl .text{font-size:22px}
    .tb-inhalt .g-titel{color:var(--ink)}
    .tb-fuss{display:flex;justify-content:space-between;gap:12px;background:var(--schild);border:1px solid var(--braun);padding:8px 14px;font:600 15px var(--mono);color:var(--ink)}
    .tb-datum{font:700 30px var(--mono);color:var(--braun);margin-bottom:10px}
    .tb-gross{font-weight:800;font-size:54px;line-height:1.08;text-transform:uppercase;letter-spacing:.02em;border-left:10px solid var(--akzent);padding-left:20px}
    .tb-unter{margin-top:18px;font-size:24px;color:var(--mute)}
    .tb-start .tb-inhalt{padding:40px}
    .tb-start .tb-gross{font-size:72px}
  `;
  document.body.innerHTML = '';
  document.documentElement.setAttribute('data-theme', 'light');
  document.head.appendChild(stil);
  document.body.appendChild(box);
}

function teilseite(e) {
  const adresse = BASIS + 'teilen/' + e.id + '.html';
  const bild = BASIS + 'teilen/bilder/' + e.id + '.jpg';
  const ziel = '../index.html#' + e.id;
  return `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(e.titel)} – Bundeswehr in Afghanistan</title>
<meta name="description" content="${esc(e.text)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Bundeswehr in Afghanistan">
<meta property="og:title" content="${esc(e.titel)}">
<meta property="og:description" content="${esc(e.text)}">
<meta property="og:url" content="${adresse}">
<meta property="og:image" content="${bild}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${esc(e.titel)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../style.css">
<script>location.replace(${JSON.stringify(ziel)});</script>
</head>
<body>
<main>
  <p><a href="${esc(ziel)}">Weiter zur Seite „Bundeswehr in Afghanistan“</a></p>
  <img src="bilder/${e.id}.jpg" width="1200" height="630" alt="${esc(e.titel)}" style="max-width:100%;height:auto">
</main>
</body>
</html>
`;
}

(async () => {
  fs.mkdirSync(BILDER, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ javaScriptEnabled: false });
  const p = await ctx.newPage();
  await p.goto(SEITE);
  const eintraege = await p.evaluate(() => Array.from(document.querySelectorAll('[data-teilen][id]')).map((k) => ({
    id: k.id,
    titel: k.getAttribute('data-titel') || document.title,
    text: k.getAttribute('data-text') || '',
    art: k.matches('figure') ? 'grafik' : k.matches('.zahl') ? 'zahl' : 'ueberschrift'
  })));
  eintraege.push({ id: 'start', art: 'start', seite: false });

  for (const e of eintraege) {
    for (const f of FORMATE) {
      await p.setViewportSize({ width: f.breite, height: f.hoehe });
      await p.goto(SEITE);
      await p.evaluate(rendern, { id: e.id, art: e.art, zoom: f.zoom[e.art], adresse: BASIS.replace(/^https:\/\//, '').replace(/\/$/, '') });
      await p.screenshot({ path: path.join(BILDER, e.id + f.endung + '.jpg'), type: 'jpeg', quality: 85 });
    }
    if (e.seite !== false) fs.writeFileSync(path.join(ZIEL, e.id + '.html'), teilseite(e));
    console.log('fertig:', e.id);
  }
  await browser.close();
})();
