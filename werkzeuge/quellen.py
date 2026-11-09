# Setzt die Kartenquellen [K1]…[K18] zwischen <!-- quellen --> und <!-- /quellen --> der Kartenseiten.
# Aufruf im Repo-Ordner: python3 werkzeuge/quellen.py karte.html regionalkommandos.html rc-nord.html
Q = {
'k1': 'Natural Earth: <a href="https://www.naturalearthdata.com/">Free vector and raster map data</a>, Maßstab 1:10 Mio., Länder, Provinzen und Orte. Gemeinfrei (<a href="https://github.com/nvkelso/natural-earth-vector/blob/master/LICENSE.md">Nutzungsbedingungen</a>). Kartengrundlage aller Karten, abgerufen 07.11.2026.',
'k2': 'Bundeszentrale für politische Bildung: <a href="https://www.bpb.de/kurz-knapp/lexika/kosmos-weltalmanach/65620/afghanistan/">Afghanistan</a>. KOSMOS Welt-Almanach &amp; Atlas 2025, Stuttgart 2024; Seite aktualisiert 14.04.2026.',
'k3': 'Bjørn Johannessen, Arne Strand: <a href="https://snl.no/Afghanistan">Afghanistan</a>. Store norske leksikon, aktualisiert 15.09.2026 (norwegisch).',
'k4': 'Bundeswehr: <a href="https://www.bundeswehr.de/de/auftrag/einsaetze/missionen/abgeschlossene-einsaetze-der-bundeswehr/afghanistan-isaf">Afghanistan – ISAF</a>. 31.12.2014.',
'k5': 'Bundeswehr: <a href="https://www.bundeswehr.de/de/meldungen/abzug-afghanistan/bundeswehr-afghanistan-2001-2010">Die Bundeswehr in Afghanistan 2001–2010</a>. Chronik, 21.06.2021.',
'k6': 'Bundeswehr: <a href="https://www.bundeswehr.de/de/meldungen/abzug-afghanistan/bundeswehr-afghanistan-2011-2021">Die Bundeswehr in Afghanistan 2011–2021</a>. Chronik, 21.06.2021.',
'k7': 'Bundesregierung: <a href="https://dserver.bundestag.de/btd/17/042/1704250.pdf">Fortschrittsbericht der Bundesregierung zur Lage in Afghanistan 2010</a>. Drucksache 17/4250, 13.12.2010 (PDF).',
'k8': 'NATO: International Security Assistance Force: Key Facts and Figures („Placemat“). Stand 14.12.2010. Gelesen als <a href="https://www.mo.gov.cz/assets/aktualni-mise/ukolove-uskupeni/14dec-2010-placemat.pdf">Kopie beim tschechischen Verteidigungsministerium</a> (PDF).',
'k9': 'NATO: <a href="https://www.nato.int/nato_static_fl2014/assets/pdf/pdf_2013_02/130220-isaf-placemat.pdf">ISAF: Key Facts and Figures</a>. Stand 19.02.2013 (PDF).',
'k10': 'ISAF: <a href="https://webarchive.library.unt.edu/web/20130216085030/http://www.isaf.nato.int/history.html">History</a>. Offizielle ISAF-Website, archiviert 16.02.2013 (englisch).',
'k11': 'ISAF: <a href="https://webarchive.library.unt.edu/web/20121006183401/http://www.isaf.nato.int/subordinate-commands/rc-north/index.php">RC – North</a>. Offizielle ISAF-Website, archiviert 06.10.2012 (englisch).',
'k12': 'GlobalSecurity.org: <a href="https://www.globalsecurity.org/military/ops/oef_orbat_isaf_1103.htm">International Security Assistance Force – ISAF (March 2011)</a>. Gliederung, Stand 04.03.2011 (englisch).',
'k13': 'StrategyPage: <a href="https://www.strategypage.com/htmw/htlead/articles/20100618.aspx">Leadership: Reorganizing NATO In Afghanistan</a>. 18.06.2010 (englisch).',
'k14': 'Wikipedia: <a href="https://en.wikipedia.org/wiki/War_in_Afghanistan_order_of_battle,_2012">War in Afghanistan order of battle, 2012</a>. Stand der Darstellung November 2012, abgerufen 07.11.2026 (englisch). Die Seite bezeichnet ihre Listen selbst als „rough and unofficial“; hier nur ergänzend genutzt.',
'k15': 'Bundeszentrale für politische Bildung: <a href="https://www.bpb.de/themen/militaer/deutsche-verteidigungspolitik/238332/der-bundeswehreinsatz-in-afghanistan/">Der Bundeswehreinsatz in Afghanistan</a>. 15.12.2016 (auf der Startseite Quelle [2]).',
'k16': 'Markus Würz: <a href="https://www.hdg.de/lemo/kapitel/globalisierung/internationale-herausforderungen/afghanistan-einsatz.html">Afghanistan-Einsatz</a>. LeMO, Stiftung Haus der Geschichte, Stand 22.06.2023 (auf der Startseite Quelle [3]).',
'k17': 'Flags of the World (CRW Flags): <a href="https://www.crwflags.com/fotw/flags/af.html">Afghanistan</a>. Seite zuletzt geändert 02.08.2025, abgerufen 09.11.2026 (englisch). Fundstelle: „Flag adopted 4 January 2004. Date on flag: 1298 = 1919 C.E.“',
'k18': 'Whitney Smith, Redaktion Encyclopaedia Britannica: <a href="https://www.britannica.com/topic/flag-of-Afghanistan">Flag of Afghanistan</a>. Ohne Datum, abgerufen 09.11.2026 (englisch). Nennt die Einführung am 29.01.2002 und die Zusätze nach der Verfassung von 2004; der Text ist in Teilen nicht aktualisiert.',
}
# Hinweis zur Unabhängigkeit (steht auf jeder Kartenseite):
GRUPPEN = '[k4], [k5], [k6] (Bundeswehr) und [k7] (Bundesregierung, mit dem Verteidigungsministerium erstellt) gelten untereinander nicht als unabhängig. Ebenso [k8], [k9], [k10] und [k11], die alle von NATO bzw. ISAF stammen.'
import sys, re
def liste(ids):
    out=['    <ul class="kliste">']
    for i in ids:
        out.append(f'      <li id="{i}"><span class="knr">[K{i[1:]}]</span> {Q[i]}</li>')
    out.append('    </ul>')
    return '\n'.join(out)
if __name__=='__main__':
  for datei in sys.argv[1:]:
    s=open(datei,encoding='utf-8').read()
    ids=sorted(set(re.findall(r'href="#(k\d+)"',s)),key=lambda x:int(x[1:]))
    a,e='<!-- quellen -->','<!-- /quellen -->'
    i,j=s.index(a)+len(a),s.index(e)
    s=s[:i]+'\n'+liste(ids)+'\n    '+s[j:]
    open(datei,'w',encoding='utf-8').write(s); print(datei, ids)
