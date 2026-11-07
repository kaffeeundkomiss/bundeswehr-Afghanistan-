# Erzeugt die drei Inline-Karten und setzt sie zwischen die Markierungen
#   <!-- karte:NAME -->  ...  <!-- /karte:NAME -->
# in karte.html, regionalkommandos.html und rc-nord.html.
# Kartengrundlage: Natural Earth (gemeinfrei), vorverarbeitet in kartendaten.json.
# Aufruf im Repo-Ordner:  python3 werkzeuge/karten.py
import json, math, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(HIER)
D = json.load(open(os.path.join(HIER, 'kartendaten.json'), encoding='utf-8'))
P = D['proj']
W, H = D['size']

def proj(lon, lat):
    return ((lon - P['lon0']) * P['k'] * P['s'], (P['lat0'] - lat) * P['s'])

# Deutsche Provinznamen (Schreibweise nach Natural Earth name_de, leicht angepasst)
NAMEN = {
 'AF-BDS':'Badachschan','AF-TAK':'Tachar','AF-KDZ':'Kundus','AF-BAL':'Balch','AF-JOW':'Dschuzdschan',
 'AF-FYB':'Faryab','AF-BDG':'Badghis','AF-HER':'Herat','AF-NIM':'Nimrus','AF-FRA':'Farah','AF-KNR':'Kunar',
 'AF-NUR':'Nuristan','AF-NAN':'Nangarhar','AF-KHO':'Chost','AF-PKA':'Paktia','AF-PIA':'Paktika','AF-ZAB':'Zabul',
 'AF-KAN':'Kandahar','AF-HEL':'Helmand','AF-URU':'Urusgan','AF-GHA':'Ghazni','AF-PAR':'Parwan','AF-KAB':'Kabul',
 'AF-LAG':'Laghman','AF-LOG':'Logar','AF-KAP':'Kapisa','AF-WAR':'Wardak','AF-BAM':'Bamiyan','AF-PAN':'Pandschir',
 'AF-SAR':'Sar-i Pul','AF-GHO':'Ghor','AF-BGL':'Baghlan','AF-SAM':'Samangan','AF-DAY':'Daikundi'}

# Zuordnung der Provinzen zu den Regionalkommandos, Stand Dezember 2010 (siehe QUELLEN.md)
RC = {
 'C': ['AF-KAB'],
 'N': ['AF-BDS','AF-TAK','AF-KDZ','AF-BAL','AF-JOW','AF-FYB','AF-SAR','AF-BGL','AF-SAM'],
 'W': ['AF-HER','AF-FRA','AF-BDG','AF-GHO'],
 'S': ['AF-KAN','AF-ZAB','AF-URU','AF-DAY'],
 'SW': ['AF-HEL','AF-NIM'],
 'E': ['AF-BAM','AF-PAR','AF-PAN','AF-KAP','AF-LAG','AF-NUR','AF-KNR','AF-NAN','AF-WAR','AF-LOG','AF-PKA','AF-KHO','AF-PIA','AF-GHA'],
}
# Zuordnung nur durch eine Quelle belegt
UNSICHER = {'AF-DAY'}
RC_VON = {p: r for r, ps in RC.items() for p in ps}

# Orte: Koordinaten aus Natural Earth populated places; Bagram ungefähr (nicht in Natural Earth)
ORTE = {
 'kabul': ('Kabul', 69.181, 34.519), 'kundus': ('Kundus', 68.873, 36.728),
 'feyzabad': ('Faisabad', 70.579, 37.130), 'masar': ('Masar-i-Scharif', 67.100, 36.700),
 'termes': ('Termes', 67.273, 37.233), 'meymaneh': ('Maimana', 64.770, 35.930),
 'polekhomri': ('Pol-e Chomri', 68.701, 35.951), 'sheberghan': ('Scheberghan', 65.738, 36.658),
 'herat': ('Herat', 62.170, 34.330), 'kandahar': ('Kandahar', 65.695, 31.610),
 'lashkargah': ('Laschkar Gah', 64.360, 31.583), 'bagram': ('Bagram', 69.27, 34.95),
}

def f(x): return f'{x:.1f}'

def nachbarn(ausser=('AFG',)):
    teile = []
    for iso, n in D['neighbors'].items():
        if iso in ausser or not n['d']:
            continue
        teile.append(f'<path class="land" d="{n["d"]}"/>')
    return '\n'.join(teile)

def land_namen():
    # feste Positionen für Nachbarstaaten (Startwerte, von Hand gesetzt)
    pos = {'Pakistan': (69.3, 30.3), 'Turkmenistan': (61.2, 37.6),
           'Usbekistan': (65.6, 38.2), 'Tadschikistan': (69.0, 38.35), 'China': (75.0, 37.4)}
    out = []
    for name, (lon, lat) in pos.items():
        x, y = proj(lon, lat)
        out.append(f'<text class="landname" x="{f(x)}" y="{f(y)}">{name}</text>')
    x, y = proj(60.05, 33.0)
    out.append(f'<text class="landname" x="{f(x)}" y="{f(y)}" transform="rotate(-90 {f(x)} {f(y)})">Iran</text>')
    return '\n'.join(out)

def ort(key, cls='ort', dx=3, dy=-2, anker='start', label=None):
    name, lon, lat = ORTE[key]
    x, y = proj(lon, lat)
    t = label or name
    return (f'<g class="{cls}"><circle cx="{f(x)}" cy="{f(y)}" r="1.9"/>'
            f'<text x="{f(x+dx)}" y="{f(y+dy)}" text-anchor="{anker}">{t}</text></g>')

def svg(inhalt, titel, desc, vb=None, cls=''):
    vb = vb or f'-6 -4 {f(W+12)} {f(H+8)}'
    return (f'<svg class="kartesvg {cls}" viewBox="{vb}" role="img" aria-labelledby="t-{cls} d-{cls}">'
            f'<title id="t-{cls}">{titel}</title><desc id="d-{cls}">{desc}</desc>\n{inhalt}\n</svg>')

def provinzen(klasse_von, beschriften=None):
    out = []
    for code, p in D['provinces'].items():
        k = klasse_von(code)
        out.append(f'<path class="prov {k}" data-prov="{code}" d="{p["d"]}"><title>{NAMEN[code]}</title></path>')
    if beschriften:
        for code in beschriften:
            x, y = D['provinces'][code]['c']
            dx, dy = beschriften[code]
            out.append(f'<text class="provname" x="{f(x+dx)}" y="{f(y+dy)}">{NAMEN[code]}</text>')
    return '\n'.join(out)

# ---------- Karte 1: Übersicht ----------
def karte_uebersicht():
    inhalt = '\n'.join([
        nachbarn(),
        provinzen(lambda c: 'afg'), land_namen(),
        f'<text class="gebirge" x="{f(proj(68.6,35.55)[0])}" y="{f(proj(68.6,35.55)[1])}" transform="rotate(-24 {f(proj(68.6,35.55)[0])} {f(proj(68.6,35.55)[1])})">H I N D U K U S C H</text>',
        ort('kabul', 'ort haupt', 3, 4, label='Kabul'),
        ort('masar', 'ort de', -2, -4, 'middle'),
        ort('kundus', 'ort de', 3, 4),
        ort('feyzabad', 'ort de', 3, -2),
        ort('termes', 'ort de', 3, -2, label='Termes (Usbekistan)'),
        ort('herat', 'ort', 3, -2), ort('kandahar', 'ort', 3, -2),
    ])
    return svg(inhalt, 'Karte Afghanistans mit Nachbarstaaten und Standorten der Bundeswehr',
               'Afghanistan mit seinen 34 Provinzen und den sechs Nachbarstaaten. Hervorgehoben sind Kabul, Masar-i-Scharif, Kundus, Faisabad und Termes in Usbekistan.',
               cls='uebersicht')

# ---------- Karte 2: Regionalkommandos ----------
def karte_rc():
    lab = {'N': ('RC North', 66.9, 36.1), 'W': ('RC West', 63.2, 33.6),
           'S': ('RC South', 66.2, 32.0), 'SW': ('RC Southwest', 63.0, 30.9), 'E': ('RC East', 69.6, 33.3)}
    tx = []
    for r, (t, lon, lat) in lab.items():
        x, y = proj(lon, lat)
        tx.append(f'<text class="rcname" x="{f(x)}" y="{f(y)}">{t}</text>')
    inhalt = '\n'.join([
        nachbarn(),
        '<defs><pattern id="schraffur" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        '<rect width="3" height="3" style="fill:var(--k-afg)"/><rect width="1.5" height="3" style="fill:var(--rc-s)"/></pattern></defs>',
        provinzen(lambda c: 'rc-' + RC_VON[c].lower() + (' unsicher' if c in UNSICHER else '')), land_namen(),
        '\n'.join(tx),
        ort('masar', 'ort hq', 0, -3.5, 'middle'), ort('herat', 'ort hq', 0, -3.5, 'middle'),
        ort('kandahar', 'ort hq', 3, 4), ort('lashkargah', 'ort hq', -3, 4.5, 'end'),
        ort('bagram', 'ort hq', 3, -2), ort('kabul', 'ort hq rcc', -3.2, 1.4, 'end', 'RC Capital · Kabul'),
    ])
    return svg(inhalt, 'Karte der ISAF-Regionalkommandos, Stand Dezember 2010',
               'Afghanistan, eingeteilt in sechs ISAF-Regionalkommandos: Capital um Kabul, North, West, South, Southwest und East, jeweils mit Hauptquartier.',
               cls='rc')

# ---------- Karte 3: RC North ----------
def karte_nord():
    prt = {  # Provinz -> Nation des PRT laut Placemat 12/2010
        'AF-BAL': 'swe', 'AF-BDS': 'deu', 'AF-KDZ': 'deu', 'AF-BGL': 'hun', 'AF-FYB': 'nor', 'AF-JOW': 'tur'}
    def kl(c):
        if RC_VON[c] != 'N':
            return 'aussen'
        return 'nord ' + ('prt-' + prt[c] if c in prt else 'ohne')
    nordcodes = RC['N']
    # Ausschnitt um den Norden
    xs, ys = [], []
    for c in nordcodes:
        for m in re.finditer(r'(-?\d+\.\d) (-?\d+\.\d)', D['provinces'][c]['d']):
            xs.append(float(m.group(1))); ys.append(float(m.group(2)))
    x0, y0, x1, y1 = min(xs) - 4, min(ys) - 9, max(xs) + 4, max(ys) + 4
    vb = f'{f(x0)} {f(y0)} {f(x1-x0)} {f(y1-y0)}'
    beschr = {c: (0, 0) for c in nordcodes}
    beschr.update({'AF-BDS': (-3, 5), 'AF-BAL': (1, 9), 'AF-SAR': (0, 3), 'AF-KDZ': (-1.5, 6.5), 'AF-TAK': (0, 2),
                   'AF-BGL': (0, 5.5), 'AF-FYB': (3, 7), 'AF-JOW': (2, 6.5), 'AF-SAM': (0, 1)})
    inhalt = '\n'.join([
        nachbarn(),
        provinzen(kl, beschr),
        ort('masar', 'ort prt', 0, 4.2, 'middle', 'Masar-i-Scharif · SWE'),
        ort('feyzabad', 'ort prt', 0, -3, 'middle', 'Faisabad · DEU'),
        ort('kundus', 'ort prt', 2.5, -2.2, 'start', 'Kundus · DEU'),
        ort('polekhomri', 'ort prt', 2.5, -1.5, 'start', 'Pol-e Chomri · HUN'),
        ort('meymaneh', 'ort prt', 0, -3, 'middle', 'Maimana · NOR'),
        ort('sheberghan', 'ort prt', -2.5, -2.2, 'end', 'Scheberghan · TUR'),
        ort('termes', 'ort', 0, -3, 'middle', 'Termes (Usbekistan)'),
    ])
    return svg(inhalt, 'Karte des Regionalkommandos Nord mit Wiederaufbauteams, Stand Dezember 2010',
               'Die neun Provinzen des Regionalkommandos Nord. Markiert sind die sechs Wiederaufbauteams mit der Nation, die sie stellte: Masar-i-Scharif Schweden, Faisabad und Kundus Deutschland, Pol-e Chomri Ungarn, Maimana Norwegen, Scheberghan Türkei.',
               vb=vb, cls='nord')

def einsetzen(datei, name, svgtext):
    pfad = os.path.join(WURZEL, datei)
    s = open(pfad, encoding='utf-8').read()
    a, e = f'<!-- karte:{name} -->', f'<!-- /karte:{name} -->'
    i, j = s.index(a) + len(a), s.index(e)
    s = s[:i] + '\n' + svgtext + '\n' + s[j:]
    open(pfad, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    einsetzen('karte.html', 'uebersicht', karte_uebersicht())
    einsetzen('regionalkommandos.html', 'rc', karte_rc())
    einsetzen('rc-nord.html', 'nord', karte_nord())
    print('Karten eingesetzt.')
