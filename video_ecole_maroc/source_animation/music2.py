import numpy as np, wave
sr=44100; D=56.5; t=np.arange(int(sr*D))/sr; out=np.zeros_like(t)
bpm=92; beat=60/bpm; bar=4*beat
def note(n): return 440*2**((n-69)/12)
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
for i in range(int(D/bar)+1):
    s=i*bar; ch=chords[i%4]
    m=(t>=s)&(t<s+bar+0.6); tt=t[m]-s
    env=np.minimum(tt/0.8,1)*np.exp(-np.maximum(tt-bar,0)*4)
    for n in ch+[ch[0]-12]:
        f=note(n); out[m]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2.003*f*tt))
    # arpeggio plucks (8th notes)
    for k in range(8):
        ps=s+k*beat/2; pm=(t>=ps)&(t<ps+0.6); pt=t[pm]-ps
        n=(ch+[ch[0]+12])[ [0,1,2,3,2,1,2,3][k] ]+12
        out[pm]+=0.035*np.exp(-pt*7)*np.sin(2*np.pi*note(n)*pt)
# kick & hat from 7s to 55.5s
for b in np.arange(7.1, 51.1, beat):
    m=(t>=b)&(t<b+0.35); kt=t[m]-b
    out[m]+=0.22*np.exp(-kt*14)*np.sin(2*np.pi*(50+90*np.exp(-kt*30))*kt)
rng=np.random.default_rng(1)
for b in np.arange(7.1+beat/2, 51.1, beat):
    m=(t>=b)&(t<b+0.05); ht=t[m]-b
    out[m]+=0.025*np.exp(-ht*80)*rng.standard_normal(m.sum())
# whooshes at cuts
for c in [7.1,11.8,17.9,20.0,21.8,27.4,29.6,33.9,38.3,44.1,47.9,51.1]:
    m=(t>=c-0.45)&(t<c+0.25); wt=t[m]-(c-0.45)
    env=np.sin(np.pi*np.clip(wt/0.7,0,1))**2
    nz=rng.standard_normal(m.sum()); nz=np.convolve(nz,np.ones(6)/6,'same')
    out[m]+=0.06*env*nz
# final hit + fade
m=t>=51.1; ft=t[m]-51.1
out[m]+=0.12*np.exp(-ft*1.5)*np.sin(2*np.pi*note(45)*ft)
out*=np.clip((D-t)/2.5,0,1)*np.clip(t/0.3,0,1)
out=out/np.max(np.abs(out))*0.7
st=np.stack([out,np.roll(out,240)],1)
w=wave.open('music2.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
