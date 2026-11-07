# bundeswehr-afghanistan

Statische Seite zum Einsatz der Bundeswehr in Afghanistan 2001–2021: Kennzahlen, Zeitleiste, Luftangriff bei Kundus, Aufarbeitung. Jede Angabe verweist auf ihre Quellen; Angaben mit nur einer Quelle sind gekennzeichnet.

- `index.html`: Startseite (kein Framework, kein Build)
- `karte.html`, `regionalkommandos.html`, `rc-nord.html`: Kartenseiten (Übersicht, ISAF-Regionalkommandos, deutsch geführter Norden)
- `werkzeuge/`: `karten.py` erzeugt die Inline-Karten aus `kartendaten.json` (Natural Earth, gemeinfrei), `quellen.py` setzt die Quellenlisten [K1]–[K16]. Nach Änderungen: `python3 werkzeuge/karten.py && python3 werkzeuge/quellen.py karte.html regionalkommandos.html rc-nord.html`
- `seite.js`: interaktive Teile (Zeitachse mit Filter, Quellen als Einblendung, antippbare Karten); ohne JavaScript bleibt alles lesbar
- `style.css`: Gestaltung, heller und dunkler Modus
- `QUELLEN.md`: Belegmatrix mit Fundstellen und offenen Punkten
- `ANLEITUNG.md`: Repository anlegen, GitHub Pages einschalten, ins Projekt „Geschichte“ aufnehmen

Lokal ansehen: `index.html` im Browser öffnen.
