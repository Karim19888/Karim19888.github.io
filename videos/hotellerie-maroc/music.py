"""Bande-son procédurale (aucun sample externe) — mode Hijaz sur Ré, bendir, oud synthétique.
Usage: python3 music.py out.wav
"""
import sys, wave
import numpy as np

SR = 44100
DUR = 42.0
BPM = 120
BEAT = 60 / BPM
BOUNDS = [4.6, 11, 16, 20.5, 25.5, 31.5, 38]
rng = np.random.default_rng(7)
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)

def hz(semi, base=146.83):  # D3
    return base * 2 ** (semi / 12)

HIJAZ = [0, 1, 4, 5, 7, 8, 10, 12]

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l
    R[i:i + len(sig)] += sig * gain * r

def env(n, a=0.01, rel=0.2):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(rel * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e

def pluck(f, dur=1.6, bright=0.6, decay=0.996):
    """Karplus-Strong vectorisé par période -> timbre type oud."""
    n = int(dur * SR); P = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, P)
    # adoucir l'attaque (plectre)
    for _ in range(int((1 - bright) * 4)):
        buf = 0.5 * (buf + np.roll(buf, 1))
    out = np.zeros(n + P); out[:P] = buf
    k = P
    while k < n:
        prev = out[k - P:k]
        nxt = decay * 0.5 * (prev + np.concatenate(([out[k - P - 1] if k - P - 1 >= 0 else 0], prev[:-1])))
        m = min(P, n - k); out[k:k + m] = nxt[:m]; k += P
    s = out[:n] * env(n, 0.002, 0.3)
    return s * 0.6

def pad(freqs, dur, a=1.5, rel=2.0):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.13):
            ff = f * 2 ** (det / 12)
            s += np.sin(2 * np.pi * ff * t + rng.uniform(0, 6)) + 0.25 * np.sin(4 * np.pi * ff * t)
    s *= (0.85 + 0.15 * np.sin(2 * np.pi * 0.2 * t))
    return s / (len(freqs) * 3) * env(n, a, rel)

def dum(gain=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 55 + 70 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    s += 0.15 * rng.uniform(-1, 1, n) * np.exp(-t * 60)
    return s * gain

def tek(gain=0.5):
    n = int(0.12 * SR); t = np.arange(n) / SR
    nz = rng.uniform(-1, 1, n); nz = nz - np.concatenate(([0], nz[:-1]))  # passe-haut simple
    s = nz * np.exp(-t * 45) + 0.4 * np.sin(2 * np.pi * 420 * t) * np.exp(-t * 40)
    return s * gain

def shaker(gain=0.12):
    n = int(0.06 * SR); t = np.arange(n) / SR
    nz = rng.uniform(-1, 1, n); nz = nz - np.concatenate(([0], nz[:-1]))
    return nz * np.exp(-t * 70) * gain

def whoosh(dur=0.9, gain=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    nz = rng.uniform(-1, 1, n)
    # filtre passe-bas glissant (one-pole) dont la coupure monte puis descend
    cut = 0.02 + 0.5 * np.sin(np.pi * t / dur) ** 2
    y = np.zeros(n); acc = 0.0
    for i in range(n):
        acc += cut[i] * (nz[i] - acc); y[i] = acc
    return y * np.sin(np.pi * t / dur) ** 1.5 * gain

def boom(gain=1.0):
    n = int(2.5 * SR); t = np.arange(n) / SR
    f = 40 + 50 * np.exp(-t * 10)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.8)
    return s * gain

# ---------------- arrangement (Reel ~42 s, 120 BPM) ----------------
for t0, t1, g in [(0, 4.6, 0.2), (4.6, 25.5, 0.12), (25.5, 31.5, 0.16), (31.5, 42, 0.15)]:
    add(pad([hz(-12), hz(-5)], t1 - t0 + 1.0, a=0.3, rel=1.0), t0, g)

# Hook: 3 impacts + stamp, cluster tendu
add(pad([hz(0), hz(1), hz(4)], 4.8, a=0.2, rel=0.4), 0, 0.12)
for i, h in enumerate([0, 0.6, 1.2]):
    add(dum(1.0), h, 1.0); add(boom(0.5), h, 0.35); add(pluck(hz([0, 1, 4][i] + 12), 0.8, bright=0.9), h, 0.6)
add(whoosh(0.5, 0.4), 1.4, 1.0)
add(boom(1.0), 2.45, 0.9); add(tek(0.9), 2.45, 0.9)
for k, d in enumerate([7, 8, 7, 4, 1, 0]):
    add(pluck(hz(d), 1.0), 2.8 + k * 0.25, 0.5, pan=-0.3 + 0.1 * k)

# Groove 4.6 -> 38 (allégé pendant les chiffres)
ARP = [0, 4, 5, 7, 8, 7, 5, 4, 0, 4, 7, 12, 10, 8, 7, 4]
t = 4.6; step = 0
while t < 38:
    beat_pos = step % 8
    light = 25.5 <= t < 28.6
    if beat_pos in (0, 3, 5) and not light: add(dum(1.0), t, 0.75)
    if beat_pos == 4: add(dum(0.8), t, 0.5)
    if beat_pos in (2, 6, 7) and not light: add(tek(), t, 0.5, pan=0.3)
    add(shaker(), t, 1.0, pan=-0.4); add(shaker(0.07), t + BEAT / 4, 1.0, pan=-0.4)
    semi = ARP[step % 16] + (12 if t >= 31.5 and step % 2 == 0 else 0)
    add(pluck(hz(semi), 0.9, bright=0.75 if t < 31.5 else 0.9), t, 0.32, pan=0.25 if step % 2 else -0.25)
    if beat_pos == 0:
        add(pluck(hz(-12 + (5 if (step // 16) % 4 == 2 else 0), 146.83), 1.2, bright=0.3, decay=0.998), t, 0.6)
    t += BEAT / 2; step += 1

# Accents synchronisés
for h in [8.7, 11.3, 13.1, 16.3, 16.9, 17.5, 28.6]:
    add(tek(0.8), h, 0.7); add(dum(0.9), h, 0.6)
add(boom(0.8), 14.6, 0.7)
for i, d in enumerate([0, 4, 7, 12, 16]):
    add(pluck(hz(d), 1.0, bright=0.9), 26.0 + i * 0.26, 0.45)
add(boom(0.6), 27.3, 0.5)
add(pad([hz(0), hz(7), hz(12), hz(16)], 10, a=1.0, rel=3.0), 31.5, 0.12)
add(whoosh(1.0, 0.4), 34.3, 1.0); add(boom(1.0), 35.2, 1.0)
for i, d in enumerate([12, 16, 19, 24]):
    add(pluck(hz(d), 2.0, bright=0.9, decay=0.998), 35.9 + i * 0.15, 0.4, pan=-0.3 + 0.2 * i)
for i, d in enumerate([0, 7, 12, 16, 19]):
    add(pluck(hz(d), 3.0, bright=0.6, decay=0.999), 38.1 + i * 0.3, 0.35, pan=-0.4 + 0.2 * i)

# Transitions
for b in BOUNDS:
    add(whoosh(0.45, 0.3), b - 0.3, 1.0, pan=0.5)
    add(whoosh(0.45, 0.3), b - 0.28, 1.0, pan=-0.5)

# ---------------- master ----------------
tt = np.arange(N) / SR
fade = np.clip(tt / 0.3, 0, 1) * np.clip((DUR - tt) / 2.5, 0, 1)
mix = np.stack([L, R], 1) * fade[:, None]
mix = np.tanh(mix * 1.4) / np.tanh(1.4)  # saturation douce
mix /= np.max(np.abs(mix)) / 0.89
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok', DUR, 's')
