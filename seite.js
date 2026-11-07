/* Interaktive Teile aller Seiten. Ohne JavaScript bleibt alles lesbar:
   Zeitleiste als Liste, Quellenverweise als Sprungmarken, Karten als Bild. */
(function () {
  'use strict';

  var ARTEN = {
    bundestag: 'Bundestag',
    einsatz: 'Einsatz',
    gewalt: 'Anschläge und Gefechte',
    aufarbeitung: 'Aufarbeitung'
  };

  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }

  function jahrAnteil(datum) {
    var t = datum.split('-');
    var j = +t[0], m = t[1] ? +t[1] - 1 : 6, d = t[2] ? +t[2] : 15;
    return j + (m * 30.4 + d) / 365;
  }

  /* ---------- Zeitleiste ---------- */
  function zeitleiste(ol) {
    var punkte = Array.prototype.slice.call(ol.querySelectorAll('li[data-datum]'));
    if (punkte.length < 3) return;
    var werte = punkte.map(function (li) { return jahrAnteil(li.getAttribute('data-datum')); });
    var von = Math.floor(Math.min.apply(null, werte));
    var bis = Math.ceil(Math.max.apply(null, werte) + 0.01);
    var spanne = bis - von;

    var box = el('div', { class: 'zl-steuerung' });
    var HINWEIS = 'Punkt auf der Zeitachse antippen, um zum Eintrag zu springen.';
    var hinweis = el('p', { class: 'zl-hinweis', 'aria-live': 'polite' }, HINWEIS);

    // Filter, nur wenn mehrere Arten vorkommen
    var arten = [];
    punkte.forEach(function (li) {
      var a = li.getAttribute('data-art');
      if (a && arten.indexOf(a) < 0) arten.push(a);
    });
    var filterLeiste = null;
    if (arten.length > 1) {
      filterLeiste = el('div', { class: 'zl-filter', role: 'group', 'aria-label': 'Einträge filtern' });
      var alle = el('button', { type: 'button', 'aria-pressed': 'true', 'data-art': '' }, 'Alle');
      filterLeiste.appendChild(alle);
      Object.keys(ARTEN).forEach(function (a) {
        if (arten.indexOf(a) < 0) return;
        var b = el('button', { type: 'button', 'aria-pressed': 'false', 'data-art': a });
        b.appendChild(el('span', { class: 'zl-farbe art-' + a, 'aria-hidden': 'true' }));
        b.appendChild(document.createTextNode(ARTEN[a]));
        filterLeiste.appendChild(b);
      });
      box.appendChild(filterLeiste);
    }

    // Achse
    var achse = el('div', { class: 'zl-achse' });
    var linie = el('div', { class: 'zl-linie', 'aria-hidden': 'true' });
    achse.appendChild(linie);
    var schritt = spanne > 12 ? 5 : 2;
    for (var j = Math.ceil(von / schritt) * schritt; j <= bis; j += schritt) {
      var m = el('span', { class: 'zl-jahr', 'aria-hidden': 'true' }, String(j));
      m.style.left = ((j - von) / spanne * 100) + '%';
      achse.appendChild(m);
    }
    var knoepfe = [];
    punkte.forEach(function (li, i) {
      if (!li.id) li.id = 'zl-' + li.getAttribute('data-datum') + '-' + i;
      li.setAttribute('tabindex', '-1');
      var art = li.getAttribute('data-art') || '';
      if (art) li.classList.add('art-' + art);
      var zeit = li.querySelector('time');
      var b = el('button', {
        type: 'button', class: 'zl-punkt art-' + art,
        'aria-label': (zeit ? zeit.textContent + ': ' : '') + (ARTEN[art] || 'Eintrag'),
        'data-ziel': li.id
      });
      b.style.left = ((werte[i] - von) / spanne * 100) + '%';
      b.addEventListener('click', function () { waehle(li, true); });
      b.addEventListener('mouseenter', function () { vorschau(li); });
      b.addEventListener('focus', function () { vorschau(li); });
      b.addEventListener('mouseleave', vorschauAus);
      b.addEventListener('blur', vorschauAus);
      achse.appendChild(b);
      knoepfe.push(b);
    });
    box.appendChild(achse);
    box.appendChild(hinweis);

    // Vor/Zurück
    var nav = el('div', { class: 'zl-schritte' });
    var zurueck = el('button', { type: 'button' }, '‹ früher');
    var vor = el('button', { type: 'button' }, 'später ›');
    nav.appendChild(zurueck); nav.appendChild(vor);
    box.appendChild(nav);

    ol.parentNode.insertBefore(box, ol);
    ol.classList.add('zl-aktiv');

    // Punkte, die sich überdecken würden, auf Spuren verteilen
    var SPUREN = [43, 23, 3];
    function verteilen() {
      var breite = achse.clientWidth, letzte = [-99, -99, -99];
      knoepfe.forEach(function (k, i) {
        if (k.hidden) return;
        var x = (werte[i] - von) / spanne * breite, s = 0;
        while (s < SPUREN.length - 1 && x - letzte[s] < 19) s++;
        letzte[s] = x;
        k.style.top = SPUREN[s] + 'px';
      });
    }
    verteilen();
    window.addEventListener('resize', verteilen);

    var aktiv = null;
    function sichtbar() { return punkte.filter(function (li) { return !li.hidden; }); }
    function waehle(li, springen) {
      if (aktiv) aktiv.classList.remove('gewaehlt');
      knoepfe.forEach(function (k) { k.classList.toggle('gewaehlt', k.getAttribute('data-ziel') === li.id); });
      aktiv = li; li.classList.add('gewaehlt'); vorschau(li);
      if (springen) {
        li.scrollIntoView({ behavior: bewegung() ? 'smooth' : 'auto', block: 'center' });
        li.focus({ preventScroll: true });
      }
    }
    function schrittweise(r) {
      var s = sichtbar(); if (!s.length) return;
      var i = aktiv ? s.indexOf(aktiv) : -1;
      i = i < 0 ? (r > 0 ? 0 : s.length - 1) : Math.max(0, Math.min(s.length - 1, i + r));
      waehle(s[i], true);
    }
    zurueck.addEventListener('click', function () { schrittweise(-1); });
    vor.addEventListener('click', function () { schrittweise(1); });

    function kurz(li) {
      var zeit = li.querySelector('time');
      var text = li.querySelector('div');
      var satz = text ? text.textContent.replace(/\s*\[\d+\][\s\S]*$/, '').split(/\.\s/)[0].replace(/\.$/, '') + '.' : '';
      return (zeit ? zeit.textContent + ': ' : '') + satz;
    }
    function vorschau(li) { hinweis.textContent = kurz(li); hinweis.classList.add('vorschau'); }
    function vorschauAus() {
      if (aktiv) { hinweis.textContent = kurz(aktiv); return; }
      hinweis.textContent = HINWEIS; hinweis.classList.remove('vorschau');
    }

    if (filterLeiste) {
      filterLeiste.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        var art = b.getAttribute('data-art');
        Array.prototype.forEach.call(filterLeiste.querySelectorAll('button'), function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        punkte.forEach(function (li, i) {
          var zeigen = !art || li.getAttribute('data-art') === art;
          li.hidden = !zeigen;
          knoepfe[i].hidden = !zeigen;
        });
        verteilen();
      });
    }
  }

  function bewegung() {
    return !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  /* ---------- Quellenverweise als Einblendung ---------- */
  function quellenEinblendung() {
    var pop = el('div', { class: 'quelle-pop', role: 'dialog', 'aria-label': 'Quelle' });
    pop.hidden = true;
    document.body.appendChild(pop);
    var offenFuer = null;

    function schliessen() {
      pop.hidden = true;
      if (offenFuer) offenFuer.setAttribute('aria-expanded', 'false');
      offenFuer = null;
    }

    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#q"], a[href^="#k"]');
      if (a && !a.closest('.quellen, .quelle-pop')) {
        var id = a.getAttribute('href').slice(1);
        var ziel = document.getElementById(id);
        if (!ziel || ziel.tagName !== 'LI') return;
        e.preventDefault();
        if (offenFuer === a) { schliessen(); return; }
        pop.innerHTML = '';
        var inhalt = ziel.cloneNode(true);
        inhalt.removeAttribute('id');
        var knr = inhalt.querySelector('.knr'); if (knr) knr.remove();
        pop.appendChild(el('div', { class: 'quelle-nr' }, a.textContent.trim()));
        var body = el('div', { class: 'quelle-text' });
        while (inhalt.firstChild) body.appendChild(inhalt.firstChild);
        pop.appendChild(body);
        var unten = el('div', { class: 'quelle-fuss' });
        var link = el('a', { href: '#' + id }, 'In der Quellenliste zeigen');
        link.addEventListener('click', function (ev) {
          ev.preventDefault(); schliessen();
          ziel.scrollIntoView({ behavior: bewegung() ? 'smooth' : 'auto', block: 'center' });
          history.replaceState(null, '', '#' + id);
          ziel.classList.add('blinkt'); setTimeout(function () { ziel.classList.remove('blinkt'); }, 1600);
        });
        var zu = el('button', { type: 'button', class: 'quelle-zu', 'aria-label': 'Schließen' }, '×');
        zu.addEventListener('click', schliessen);
        unten.appendChild(link); unten.appendChild(zu);
        pop.appendChild(unten);
        if (offenFuer) offenFuer.setAttribute('aria-expanded', 'false');
        offenFuer = a; a.setAttribute('aria-expanded', 'true');
        pop.hidden = false;
        platzieren(a);
        return;
      }
      if (!e.target.closest('.quelle-pop')) schliessen();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && offenFuer) { var a = offenFuer; schliessen(); a.focus(); }
    });
    window.addEventListener('resize', schliessen);

    function platzieren(a) {
      var r = a.getBoundingClientRect();
      var w = Math.min(360, document.documentElement.clientWidth - 24);
      pop.style.width = w + 'px';
      var x = Math.max(12, Math.min(r.left + window.scrollX - 20, window.scrollX + document.documentElement.clientWidth - w - 12));
      pop.style.left = x + 'px';
      var h = pop.offsetHeight;
      var oben = r.top - h - 8 > 0;
      pop.style.top = (oben ? r.top + window.scrollY - h - 8 : r.bottom + window.scrollY + 8) + 'px';
    }
  }

  /* ---------- Karten ---------- */
  function karten() {
    Array.prototype.forEach.call(document.querySelectorAll('.kartenrahmen'), function (fig) {
      var svg = fig.querySelector('svg.kartesvg');
      if (!svg) return;
      var info = el('p', { class: 'karten-info', 'aria-live': 'polite' }, 'Provinz antippen oder mit der Maus darauf zeigen.');
      var box = fig.querySelector('.kartenbox') || svg;
      box.parentNode.insertBefore(info, box.nextSibling);
      var provinzen = svg.querySelectorAll('.prov');
      var gewaehlt = null;
      Array.prototype.forEach.call(provinzen, function (p) {
        var t = p.querySelector('title');
        var text = p.getAttribute('data-info') || (t ? t.textContent : '');
        p.setAttribute('tabindex', '0');
        p.setAttribute('role', 'button');
        p.setAttribute('aria-label', text);
        function zeige() { info.textContent = text; }
        p.addEventListener('mouseenter', zeige);
        p.addEventListener('focus', zeige);
        p.addEventListener('click', function () {
          if (gewaehlt) gewaehlt.classList.remove('gewaehlt');
          gewaehlt = p; p.classList.add('gewaehlt'); zeige();
        });
        p.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); p.dispatchEvent(new MouseEvent('click')); }
        });
      });
      // Legende: Regionalkommando hervorheben
      var legende = fig.querySelector('.legende[data-hebt]');
      if (legende) {
        Array.prototype.forEach.call(legende.querySelectorAll('li[data-rc]'), function (li) {
          var rc = li.getAttribute('data-rc');
          var b = el('button', { type: 'button', class: 'legende-knopf', 'aria-pressed': 'false' });
          while (li.firstChild) b.appendChild(li.firstChild);
          li.appendChild(b);
          b.addEventListener('click', function () {
            var an = b.getAttribute('aria-pressed') !== 'true';
            Array.prototype.forEach.call(legende.querySelectorAll('.legende-knopf'), function (x) { x.setAttribute('aria-pressed', 'false'); });
            b.setAttribute('aria-pressed', String(an));
            svg.classList.toggle('hebt', an);
            Array.prototype.forEach.call(provinzen, function (p) {
              p.classList.toggle('hervor', an && p.classList.contains('rc-' + rc));
            });
            info.textContent = an ? b.textContent.trim() + ' hervorgehoben' : 'Provinz antippen oder mit der Maus darauf zeigen.';
          });
        });
      }
    });
  }

  document.querySelectorAll('ol.zeitleiste').forEach(zeitleiste);
  quellenEinblendung();
  karten();
})();
