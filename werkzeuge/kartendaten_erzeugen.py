# Erzeugt werkzeuge/kartendaten.json aus Natural Earth (gemeinfrei).
# Eingabe: Ordner mit a1.geojson (ne_10m_admin_1_states_provinces) und a0.geojson (ne_10m_admin_0_countries)
# aus https://github.com/nvkelso/natural-earth-vector/tree/master/geojson
# Aufruf: python3 werkzeuge/kartendaten_erzeugen.py <ordner> werkzeuge/kartendaten.json
# Erzeugt SVG-Pfade aus Natural Earth (gemeinfrei) für Afghanistan.
import json, math, sys
NE = sys.argv[1]
OUT = sys.argv[2]
a1 = json.load(open(NE+'/a1.geojson'))
a0 = json.load(open(NE+'/a0.geojson'))
FIX = {1159312097:'Panjshir', 1159312063:'Daykundi'}
CODE = {'Panjshir':'AF-PAN','Daykundi':'AF-DAY'}
LON0, LAT0 = 60.3, 38.6  # links oben
K = math.cos(math.radians(33.9))
S = 18.0  # px pro Grad Länge (Startwert)
def proj(lon, lat): return ((lon-LON0)*K*S, (LAT0-lat)*S)
def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1,y1),(x2,y2) = pts[0], pts[-1]
    dx,dy = x2-x1, y2-y1; L = math.hypot(dx,dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1,len(pts)-1):
        x,y = pts[i]; d = abs(dy*x-dx*y+x2*y1-y2*x1)/L
        if d > dmax: dmax, idx = d, i
    if dmax > eps:
        return dp(pts[:idx+1],eps)[:-1] + dp(pts[idx:],eps)
    return [pts[0], pts[-1]]
def rings(g):
    if g['type']=='Polygon': return g['coordinates']
    return [r for poly in g['coordinates'] for r in poly]
def path(g, eps=0.12, clip=None):
    out=[]
    for r in rings(g):
        pts=[proj(*c[:2]) for c in r]
        if clip:
            xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
            if max(xs)<clip[0] or min(xs)>clip[2] or max(ys)<clip[1] or min(ys)>clip[3]: continue
        m=len(pts)//2
        s=dp(pts[:m+1],eps)[:-1]+dp(pts[m:],eps)
        if len(s)<3: continue
        out.append('M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in s)+'Z')
    return ' '.join(out)
res={'provinces':{}, 'neighbors':{}}
for f in a1['features']:
    p=f['properties']
    if p.get('adm0_a3')!='AFG': continue
    name=FIX.get(p['ne_id'], p['name']); code=CODE.get(name,p['iso_3166_2'])
    c=[proj(*x[:2]) for x in rings(f['geometry'])[0]]
    # Schwerpunkt der größten Fläche (einfach)
    A=cx=cy=0
    for (x1,y1),(x2,y2) in zip(c,c[1:]):
        t=x1*y2-x2*y1; A+=t; cx+=(x1+x2)*t; cy+=(y1+y2)*t
    res['provinces'][code]={'name':name,'d':path(f['geometry']),'c':[round(cx/(3*A),1),round(cy/(3*A),1)]}
clip=(-40,-40,250,200)
for f in a0['features']:
    p=f['properties']; iso=p['ADM0_A3']
    if iso in ('AFG','PAK','IRN','TKM','UZB','TJK','CHN','IND','KGZ'):
        res['neighbors'][iso]={'name':p['NAME_DE'],'d':path(f['geometry'],0.15,clip)}
pts=[proj(*c) for c in [(60.3,38.6),(75.2,29.3)]]
res['size']=[round(pts[1][0],1), round(pts[1][1],1)]
res['proj']={'lon0':LON0,'lat0':LAT0,'k':K,'s':S}
json.dump(res, open(OUT,'w'), ensure_ascii=False)
print(res['size'], {k:v['c'] for k,v in list(res['provinces'].items())[:3]}, sum(len(v['d']) for v in res['provinces'].values()))
