# Bande-son synthétique : pluie + nappe + pulsation + impacts aux transitions (laisse de la place pour la voix)
import numpy as np, wave, sys
SR, D = 48000, 64
n = SR * D; t = np.arange(n) / SR; rng = np.random.default_rng(3)
def onepole(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); b = 1 - a
    out = np.empty_like(x)
    for s in range(0, len(x), SR):
        blk = x[s:s + SR]
        # récurrence y[i]=a*y[i-1]+b*x[i] résolue par convolution exponentielle tronquée
        L = int(5 / (1 - a)) + 1; L = min(L, 20000)
        h = b * a ** np.arange(L)
        out[s:s + SR] = np.convolve(np.concatenate([x[max(0, s - L):s], blk]), h)[min(s, L):min(s, L) + len(blk)]
    return out
env = lambda a, b: np.clip((t - a) / max(b - a, 1e-6), 0, 1)
SEG = [0, 6, 14, 24, 32, 41, 51, 59, 64]
# --- pluie
w = rng.standard_normal((2, n))
rain = np.stack([onepole(w[c], 3500) - onepole(w[c], 400) for c in range(2)])
crack = (rng.random((2, n)) < 0.0009) * rng.standard_normal((2, n)) * 3
rain = rain + onepole(crack[0], 6000)[None] * .5
inten = 0.55 + 0.45 * (t < 6) + 0.35 * ((t > 55) & (t < 64)) - 0.25 * ((t > 24) & (t < 32))
rain *= inten * .9
# --- nappe (ré mineur)
pad = np.zeros(n)
for f, g in [(73.42, 1), (110, .6), (174.61, .35), (146.83, .4), (220, .2)]:
    pad += g * np.sin(2 * np.pi * f * t + 2 * np.sin(2 * np.pi * .07 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * .13 * t + f))
pad *= .10 * env(0, 3) * (1 - env(62, 64))
# --- pulsation 96 bpm à partir de 6 s, plus légère pendant l'analogie
bpm = 96; beat = 60 / bpm
kick = np.zeros(n); hat = np.zeros(n)
kl = int(.35 * SR); kt = np.arange(kl) / SR
ks = np.sin(2 * np.pi * (45 + 90 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 9)
hl = int(.05 * SR); hs = rng.standard_normal(hl) * np.exp(-np.arange(hl) / SR * 80)
hs = hs - onepole(hs, 5000)
bt = 6.0
while bt < 58.9:
    i = int(bt * SR); amp = .45 if 24 <= bt < 32 else 1
    kick[i:i + kl] += ks[:n - i] * amp
    j = int((bt + beat / 2) * SR)
    if j + hl < n: hat[j:j + hl] += hs * amp
    bt += beat
# --- impacts + souffles aux transitions
hit = np.zeros(n)
for s in SEG[1:-1]:
    i = int(s * SR); L = int(1.2 * SR); tt = np.arange(L) / SR
    boom = np.sin(2 * np.pi * (38 + 40 * np.exp(-tt * 8)) * tt) * np.exp(-tt * 3.2)
    hit[i:i + L] += boom[:n - i] * .9
    wl = int(.45 * SR); ws = rng.standard_normal(wl); ws = ws - onepole(ws, 800)
    ws *= np.linspace(0, 1, wl) ** 2
    hit[i - wl:i] += ws * .35
# tonnerre au début et à la fin
for at, g in [(0.05, 1.0), (55.0, .6)]:
    i = int(at * SR); L = int(3 * SR); tt = np.arange(L) / SR
    th = onepole(rng.standard_normal(L), 180) * (np.exp(-tt * 1.2) * (1 - np.exp(-tt * 30))) * 6 * g
    hit[i:i + L] += th[:n - i]
mono = pad + kick * .5 + hat * .18 + hit * .55
mix = rain * .5 + mono[None]
mix *= (1 - env(63, 64))[None] * env(0, .15)[None]
mix = mix / np.max(np.abs(mix)) * .7  # marge pour la voix
data = (mix.T * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(data.tobytes())
