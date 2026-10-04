import numpy as np, wave
import json
W=json.load(open('warp.json'))
def inv(o):
    for i in range(1,len(W)):
        if o<=W[i][1]:
            (a,b),(c,d)=W[i-1],W[i]
            return a+(c-a)*(o-b)/(d-b) if d>b else a
    return W[-1][0]
SR = 44100; DUR = W[-1][0]; BPM = 100; beat = 60 / BPM
N = int(SR * DUR); t = np.arange(N) / SR
mix = np.zeros(N); rng = np.random.default_rng(7)

def add(sig, at, gain=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if i < N: mix[i:j] += sig[:j - i] * gain

def kick():
    d = np.arange(int(.35 * SR)) / SR
    f = 50 + 110 * np.exp(-d * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-d * 9)

def hat(dec=60):
    d = np.arange(int(.08 * SR)) / SR
    n = rng.standard_normal(len(d)); n = np.diff(n, prepend=0)  # crude high-pass
    return n * np.exp(-d * dec) * .5

def snap():
    d = np.arange(int(.2 * SR)) / SR
    n = rng.standard_normal(len(d))
    return (n * np.exp(-d * 25) + np.sin(2 * np.pi * 190 * d) * np.exp(-d * 30)) * .6

def bass(freq, length):
    d = np.arange(int(length * SR)) / SR
    env = np.minimum(1, d * 80) * np.exp(-d * 2.5)
    return (np.sin(2 * np.pi * freq * d) + .3 * np.sin(4 * np.pi * freq * d)) * env

def pluck(freq, length=.5):
    d = np.arange(int(length * SR)) / SR
    return sum(np.sin(2 * np.pi * freq * k * d) / k for k in (1, 2, 3)) * np.exp(-d * 7) * .35

def whoosh(at, length=.8):
    d = np.arange(int(length * SR)) / SR
    n = rng.standard_normal(len(d))
    # moving low-pass via cumulative smoothing with varying coefficient
    out = np.zeros_like(n); y = 0
    a = .02 + .5 * np.sin(np.pi * d / length) ** 2
    for i in range(len(n)): y += a[i] * (n[i] - y); out[i] = y
    add(out * np.sin(np.pi * d / length) ** 2 * .9, at - length / 2)

def pop(at, f=880):
    d = np.arange(int(.18 * SR)) / SR
    add(np.sin(2 * np.pi * (f + 600 * np.exp(-d * 40)) * d) * np.exp(-d * 22) * .45, at)

# A minor groove: Am - F - C - G (roots)
roots = [55.0, 43.65, 65.41, 49.0]
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
nbeats = int(DUR / beat)
for b in range(nbeats):
    at = b * beat; bar = b // 4; ch = bar % 4
    intro = at < 6
    if not intro or b % 2 == 0: add(kick(), at, .9)
    if b % 4 in (1, 3) and not intro: add(snap(), at, .45)
    add(hat(), at + beat / 2, .25); add(hat(90), at + beat * .75, .12)
    if b % 2 == 0: add(bass(roots[ch], beat * 1.8), at, .5)
    if b % 4 == 0 or b % 4 == 3:
        for k, f in enumerate(chords[ch]): add(pluck(f), at + k * .06 + (beat / 2 if b % 4 == 3 else 0), .22)

for s in (6, 13, 25, 36, 47): whoosh(inv(s))
for p, f in ((0.15, 1200), (8.0, 990), (12.0, 990), (14.7, 660), (21.8, 1320), (26.0, 990), (30.2, 1320),
             (37.1, 880), (37.7, 990), (38.2, 1100), (41.0, 1320), (53.6, 990)):
    pop(inv(p), f)
add(kick() * 1.4, inv(44.0), 1.0)  # stamp thud
# fade in/out
mix *= np.minimum(1, t / .3) * np.minimum(1, (DUR - t) / 2.0)
mix /= np.max(np.abs(mix)) / .8
st = np.stack([mix, mix], 1)
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok')
