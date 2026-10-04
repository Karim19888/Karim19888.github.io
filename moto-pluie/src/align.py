import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
# Aligne le script sur la voix : segments de parole = silencedetect (-38 dB, 0,25 s) sur voix_off_yassine_v4.mp3
txt=open(os.path.join(HERE, '../VOIX_OFF_ELEVENLABS_V4.txt')).read()
txt=re.sub(r'\[[^\]]*\]','',txt)
units=[u.strip() for u in re.split(r'(?<=[،.…:!])',txt.replace('\n',' ')) if u.strip() and re.search(r'\w',u)]
segs=[(0,3.67),(4.24,5.95),(6.37,9.14),(9.69,12.70),(13.07,16.48),(16.84,18.55),(18.81,21.30),(21.63,23.83),(24.16,25.17),(25.48,27.36),(27.71,31.19),(31.60,34.90),(35.21,36.67),(36.96,39.92),(40.26,42.55),(42.88,45.93),(46.27,49.83),(50.16,51.98),(52.25,53.58)]
L=[len(re.sub(r'[^\w]','',u)) for u in units]
k=sum(b-a for a,b in segs)/sum(L)
n,m=len(units),len(segs)
import functools
INF=1e18
@functools.lru_cache(None)
def f(i,j):
    if i==n and j==m: return (0,())
    if i==n or j==m: return (INF,())
    best=(INF,())
    s=0
    for e in range(i+1,n+1):
        s+=L[e-1]
        c,p=f(e,j+1)
        d=segs[j][1]-segs[j][0]
        c+= ((d-k*s)/max(d,.5))**2
        if c<best[0]: best=(c,((i,e),)+p)
    return best
c,p=f(0,0)
print('rate',round(1/k,1),'chars/s cost',round(c,3), len(units),'units')
for (i,e),(a,b) in zip(p,segs):
    print(f"{a:6.2f}-{b:6.2f} ({b-a:4.2f}s, pred {k*sum(L[i:e]):4.2f}) | {' '.join(units[i:e])}")

# ---------- génération de la timeline ----------
import json
OFF = 0.4
mid = lambda a, b: round((a + b) / 2 + OFF, 2)
segtxt = [' '.join(units[i:e]) for (i, e) in p]
# début de chaque scène = milieu du silence avant le premier bloc de la scène
starts = [0, mid(5.95, 6.37), mid(12.70, 13.07), mid(21.30, 21.63), mid(27.36, 27.71), mid(34.90, 35.21), mid(42.55, 42.88), mid(49.83, 50.16)]
cta_end = round(53.58 + OFF + 1.3, 2)
bounds = starts + [cta_end, round(cta_end + 5, 2)]
# sous-titres : un segment de voix, coupé en deux s'il est trop long
cues = []
for (a, b), s in zip(segs, segtxt):
    parts = [s]
    if len(s) > 34:
        us = [u for u in re.split(r'(?<=[،.…:!])\s*', s) if u.strip()]
        if len(us) > 1:
            best = min(range(1, len(us)), key=lambda k: abs(len(' '.join(us[:k])) - len(s) / 2))
            parts = [' '.join(us[:best]), ' '.join(us[best:])]
        else:
            w = s.split(); h = len(w) // 2; parts = [' '.join(w[:h]), ' '.join(w[h:])]
    tot = sum(len(x) for x in parts); cur = a
    for x in parts:
        d = (b - a) * len(x) / tot; cues.append([round(cur + OFF, 2), round(cur + d + OFF, 2), x]); cur += d
# chaque sous-titre reste jusqu'au suivant (pas de trou pendant les respirations)
for i in range(len(cues) - 1): cues[i][1] = cues[i + 1][0]
cues[-1][1] = round(cues[-1][1] + .8, 2)
json.dump({'offset': OFF, 'bounds': bounds, 'cues': cues, 'voice_segments': [[a + OFF, b + OFF] for a, b in segs]},
          open(os.path.join(HERE, 'timeline.json'), 'w'), ensure_ascii=False, indent=1)
print(bounds); print(len(cues), 'cues'); [print(c) for c in cues]
