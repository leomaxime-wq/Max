# Score, sound design and voice mix for the 30 s "24 heures" LOBBII film -> out/soundtrack.wav
import numpy as np, wave, soundfile as sf
SR=48000; D=30.0; N=int(SR*D); t=np.arange(N)/SR
rng=np.random.default_rng(1)
L=np.zeros(N); R=np.zeros(N)
def env(a,b,att=.05,rel=.3): return np.clip((t-a)/att,0,1)*np.clip((b-t)/rel,0,1)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); n=min(len(sig),N-i); L[i:i+n]+=sig[:n]*gain*(1-pan); R[i:i+n]+=sig[:n]*gain*(1+pan)
def hz(m): return 440*2**((m-69)/12)
def fftfilt(x,lo=None,hi=None):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR)
    if hi: X*=1/(1+(f/hi)**4)
    if lo: X*=1/(1+(lo/np.maximum(f,1))**4)
    return np.fft.irfft(X,len(x))
def tt(d): return np.arange(int(SR*d))/SR

# --- pad: night (dark, low) -> morning (open) -> drive -> resolve ---
chords=[(0,[38,50,57,60,65]),(4.2,[41,48,57,60,64]),(8.2,[45,52,59,64,69]),(12.7,[43,50,59,62,67]),(17.2,[41,53,60,64,69]),(20.5,[43,55,62,65,70]),(23,[46,53,62,65,69]),(25.3,[41,53,60,64,69,72])]
for k,(st,notes) in enumerate(chords):
    en=chords[k+1][0] if k+1<len(chords) else D
    e=env(st-.4,en+.7,att=1.4,rel=1.3)
    bright=.6 if st<8 else 1.0
    for m in notes:
        f=hz(m)
        for ch,det in ((0,-.0025),(1,.0025)):
            s=sum(np.sin(2*np.pi*f*(1+det)*h*t+h)/h**(2.2 if st<8 else 1.6) for h in (1,2,3,4))*bright
            (L if ch==0 else R)[:]+=s*e*.04

# --- night ambience: room tone + slow distant waves ---
w=rng.standard_normal(N); waves=fftfilt(w,lo=120,hi=900)
lfo=.5+.5*np.sin(2*np.pi*t/5.5-1.2); waves*=lfo**2/np.abs(waves).max()
amb=waves*(env(0,8.6,att=1.2,rel=1.0)*.10+env(8.2,17.6,att=.8,rel=.8)*.06)
L+=amb; R+=np.roll(amb,500)

# --- piano-like notes (soft, sparse at night) ---
def piano(f,d=2.6):
    x=tt(d); return sum(a*np.sin(2*np.pi*f*h*x)*np.exp(-x*(1.6+h*1.1)) for h,a in ((1,1),(2,.35),(3,.15),(4,.06)))*np.minimum(1,x*300)
for st,m,g in ((0.3,62,.11),(0.32,50,.07),(2.2,65,.07),(4.2,64,.07),(5.6,60,.06),(8.3,69,.08),(8.32,57,.06),(10.4,71,.05),(12.7,67,.05),(15.2,74,.05)):
    add(piano(hz(m)),st,g,pan=(.25 if m%2 else -.25))

# --- arpeggio + pulse for the dashboard section ---
def pluck(f,d=.9):
    x=tt(d); return (np.sin(2*np.pi*f*x)+.3*np.sin(2*np.pi*2*f*x)+.12*np.sin(2*np.pi*3.01*f*x))*np.exp(-x*5)
def kick():
    x=tt(.45); f=45+80*np.exp(-x*28); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*7)
def hat():
    n=np.diff(rng.standard_normal(int(SR*.08)),prepend=0); return n*np.exp(-np.arange(len(n))/SR*55)
beat=60/110; arp=[72,76,79,84,79,76]
x=13.0;i=0
while x<25.2:
    g=.035 if x<17.2 else .07
    add(pluck(hz(arp[i%6]-(3 if x>=20.5 else 0))),x,g,pan=(-.4 if i%2 else .4)); x+=beat/2; i+=1
x=17.2
while x<25.2:
    add(kick(),x,.38); add(hat(),x+beat/2,.045,pan=.3)
    if x>=20.5: add(hat(),x+beat*.75,.03,pan=-.3)
    x+=beat
ris=np.diff(rng.standard_normal(N),prepend=0)*env(22.8,25.25,att=2.3,rel=.05)**2*.09
L+=ris; R+=np.roll(ris,120)

# --- foley / UI ---
def blip(f1,f2,d=.16):
    x=tt(d); return (np.sin(2*np.pi*f1*x)*(x<d/2)+np.sin(2*np.pi*f2*x)*(x>=d/2))*np.exp(-x*18)*np.minimum(1,x*400)
def tick(): x=tt(.03); return np.sin(2*np.pi*3000*x)*np.exp(-x*200)
for k in range(16): add(tick(),2.5+k*.08,.035)                      # typing
add(blip(1250,1660),3.9,.13); add(blip(990,1320),4.85,.15)           # sent / Alfred
def knock():
    x=tt(.25); n=fftfilt(rng.standard_normal(len(x)),hi=700)
    return (n/np.abs(n).max()*.6+np.sin(2*np.pi*95*x))*np.exp(-x*38)
add(knock(),6.25,.22,pan=-.5); add(knock(),6.48,.2,pan=-.5)          # tea at the door
for k in range(14): add(tick(),7.05+ (k/14)**.7*.75,.05)             # clock fast-forward
wh=fftfilt(rng.standard_normal(int(SR*1.3)),lo=200,hi=3000); x=tt(1.3); wh*=np.sin(np.pi*x/1.3)**2
add(wh/np.abs(wh).max(),7.0,.12); add(wh/np.abs(wh).max(),16.9,.1); add(wh/np.abs(wh).max(),22.3,.1)
def bell(f,d=2.4):
    x=tt(d); return sum(a*np.sin(2*np.pi*f*r*x)*np.exp(-x*dk) for r,a,dk in ((1,1,2.2),(2.76,.4,3.5),(5.4,.2,5),(8.9,.08,7)))
add(bell(hz(84)),12.95,.07,pan=-.2); add(bell(hz(91)),13.05,.05,pan=.2)   # Victoria
for k in range(5): add(blip(1500,1500,.08),17.5+k*.3,.04,pan=.2)         # feed rows
for s0 in (18.3,19.45,20.6): add(kick(),s0,.15); add(piano(hz(57),1.2),s0,.12)   # word hits
def boom():
    x=tt(3); f=38+30*np.exp(-x*6); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*1.4)
add(boom(),25.25,.5)
for k,m in enumerate([84,88,91,96]): add(bell(hz(m),3.0),27.1+k*.07,.045,pan=(-.3+.2*k))
add(blip(990,1320),28.2,.05)

# --- voices ---
VOX=[("guest",9.2,.95,"room"),("vic",13.15,1.0,"dry"),("vo1",17.6,1.0,"dry"),("vo2",23.2,1.05,"dry"),("vo3",25.75,1.05,"dry")]
Vd=np.zeros(N); Vr=np.zeros(N)
for name,st,g,kind in VOX:
    x,sr=sf.read(f"voice/proc/{name}.wav"); assert sr==SR
    i=int(st*SR); n=min(len(x),N-i); (Vr if kind=="room" else Vd)[i:i+n]+=x[:n]*g
pk=max(np.abs(Vd).max(),np.abs(Vr).max()); Vd/=pk; Vr/=pk
V=Vd+Vr
e=(np.abs(V)>0.02).astype(float); k=int(SR*.25)
e=np.clip(np.convolve(e,np.ones(k)/k,'same')*3,0,1); e=np.convolve(e,np.ones(int(SR*.12))/int(SR*.12),'same')
duck=1-.55*e

def reverb(x,secs=2.4,seed=3,damp=3.2):
    n=int(SR*secs); x2=np.arange(n)/SR
    ir=np.random.default_rng(seed).standard_normal(n)*np.exp(-x2*damp); ir=np.convolve(ir,np.ones(6)/6,'same')
    ir[:int(SR*.012)]=0; ir/=np.sqrt((ir**2).sum())
    m=len(x)+n-1; F=1<<int(np.ceil(np.log2(m)))
    return np.fft.irfft(np.fft.rfft(x,F)*np.fft.rfft(ir,F),F)[:len(x)]
mx=max(np.abs(L).max(),np.abs(R).max()); L/=mx; R/=mx
L,R=fftfilt(L,hi=11000),fftfilt(R,hi=11000)
L=L*duck+.24*reverb(L,seed=3); R=R*duck+.24*reverb(R,seed=4)
vL=Vd+.08*reverb(Vd,1.0,5,6)+Vr*.85+.22*reverb(Vr,.7,7,7)
vR=Vd+.08*reverb(Vd,1.0,6,6)+Vr*.85+.22*reverb(Vr,.7,8,7)
L=L*.6+vL*.95; R=R*.6+vR*.95
fade=np.clip((D-t)/1.3,0,1)*np.clip(t/.15,0,1); L*=fade; R*=fade
mx=max(np.abs(L).max(),np.abs(R).max())
L=np.tanh(L/mx*1.2)/np.tanh(1.2)*.89; R=np.tanh(R/mx*1.2)/np.tanh(1.2)*.89
pcm=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open('out/soundtrack.wav','wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
print('ok')
