# Bundeswehr in Afghanistan – Einrichtung

Ziel: öffentliche Seite auf GitHub Pages, Repository im Claude-Projekt „Geschichte“.

## Phase 1: Repository anlegen (ca. 3 Min.)

1. github.com → oben rechts **+** → **New repository**
2. Repository name: `bundeswehr-afghanistan` · Sichtbarkeit: **Public** · Häkchen bei **Add a README** · **Create repository**

**Fertig wenn:** `https://github.com/kirchnerjan-cell/bundeswehr-afghanistan` öffnet sich und zeigt eine README.

## Phase 2: Dateien hochladen (ca. 3 Min.)

1. Im Repo: **Add file** → **Upload files**
2. Diese Dateien hineinziehen: `index.html`, `style.css`, `README.md`, `QUELLEN.md`, `ANLEITUNG.md` (die vorhandene README wird überschrieben)
3. **Commit changes**

**Fertig wenn:** Die Dateiliste im Repo zeigt `index.html` und `style.css`.

## Phase 3: GitHub Pages einschalten (ca. 3 Min.)

1. **Settings** (Reiter oben) → linke Spalte **Pages**
2. Source: **Deploy from a branch** · Branch: **main** · Ordner: **/ (root)** → **Save**
3. 1–2 Minuten warten, Seite neu laden

**Fertig wenn:** `https://kirchnerjan-cell.github.io/bundeswehr-afghanistan/` zeigt die Kopfzeile „Bundeswehr in Afghanistan“ und die Kennzahl 59.

## Phase 4: Ins Projekt „Geschichte“ aufnehmen

1. Claude-App → Projekt **Geschichte** öffnen
2. **Projekteinstellungen** → **Ressourcen** → Repository hinzufügen → `kirchnerjan-cell/bundeswehr-afghanistan` wählen
3. Falls das Repo nicht in der Auswahl erscheint: Die Claude-GitHub-App hat noch keinen Zugriff darauf. Unter https://github.com/apps/claude/installations/select_target das Konto wählen und das neue Repo freigeben.

Die Bezeichnungen in Schritt 2 können je nach App-Version leicht abweichen.

**Fertig wenn:** Das Repo steht in den Projekteinstellungen von „Geschichte“ unter den Ressourcen.

## Teilen-Seiten und Vorschaubilder neu erzeugen

Jede Grafik, Kennzahl und jedes Ereignis mit dem Merkmal `data-teilen` in `index.html` hat einen Teilen-Knopf. Geteilt wird die kleine Seite `teilen/<id>.html`. Sie enthält das Vorschaubild genau dieses Teils (`teilen/bilder/<id>.jpg`, 1200 × 630) und leitet Besucher zur Stelle auf der Hauptseite weiter. Der Knopf „Bild“ lädt die Hochformat-Fassung (`<id>-hoch.jpg`, 1080 × 1350) für eigene Posts. Grafiken und Kennzahlen erscheinen als Bild der Grafik, Ereignisse als gestaltete Überschrift.

Die Bilder ändern sich nicht von selbst. Nach jeder Änderung an Zahlen, Grafiken, Ereignissen oder am Stand-Datum neu erzeugen:

1. Node.js installieren (nodejs.org, LTS-Version), falls noch nicht vorhanden.
2. Im Repo-Ordner im Terminal: `npm install --no-save playwright` und danach `npx playwright install chromium`
3. `node werkzeuge/teilen.js`
4. Geänderte Dateien in `teilen/` committen.

**Fertig wenn:** Das Skript meldet für jedes Teil „fertig: <id>“, und `teilen/bilder/` enthält die neuen Bilder.

Neues teilbares Element: `id`, `data-teilen`, `data-titel` (Titel der Linkvorschau) und `data-text` (Beschreibung) ergänzen, dann Schritt 3. Optional `data-bildtext`, wenn der Text ohne die Seite nicht verständlich ist (Beispiel: „davon fielen …“).

**Linkvorschau testen** (nach dem Merge, wenn die Seite live ist): Link `…/teilen/<id>.html` im Facebook Sharing Debugger (developers.facebook.com/tools/debug) und im LinkedIn Post Inspector (linkedin.com/post-inspector) prüfen. Beide Werkzeuge erfordern eine Anmeldung. Plattformen speichern Vorschauen zwischen; nach einer Bildänderung dort „Erneut abrufen“ wählen.
