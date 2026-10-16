# Synthesized score + sound design for the 35 s LOBBII B2B trailer -> out/soundtrack.wav
import numpy as np, wave
SR=48000; D=35.0; N=int(SR*D); t=np.arange(N)/SR
rng=np.random.default_rng(1)
L=np.zeros(N); R=np.zeros(N)
def env(a,b,att=.05,rel=.3):
    e=np.clip((t-a)/att,0,1)*np.clip((b-t)/rel,0,1); return e
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); n=min(len(sig),N-i)
    L[i:i+n]+=sig[:n]*gain*(1-pan)/1; R[i:i+n]+=sig[:n]*gain*(1+pan)/1
def hz(m): return 440*2**((m-69)/12)
def lp(x,a):  # one-pole low-pass (vectorized via cumulative trick is unstable -> chunked loop)
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y

# --- pad: warm chords, slow attack ---
chords=[(0,[50,57,60,65]),(5.4,[53,60,64,69]),(11,[50,57,60,65,69]),(17,[46,53,62,65,69]),(21,[48,55,62,64,67]),(25,[45,52,60,64,67]),(28.6,[46,53,62,65,69]),(30.2,[53,60,64,67,72]),(32,[41,53,60,64,69,72])]
pad=np.zeros((2,N))
for k,(st,notes) in enumerate(chords):
    en=chords[k+1][0] if k+1<len(chords) else D
    e=env(st-.3,en+.6,att=1.2,rel=1.2)
    for m in notes:
        f=hz(m)
        for ch,det in ((0,-.0025),(1,.0025)):
            s=sum(np.sin(2*np.pi*f*(1+det)*h*t+h)/h**1.6 for h in (1,2,3,4))
            pad[ch]+=s*e
pad*=.045
L+=pad[0]; R+=pad[1]

# --- ambience 0–5.4 : soft room tone ---
w=rng.standard_normal(N); brown=np.cumsum(w); brown-=np.convolve(brown,np.ones(4801)/4801,'same'); brown/=np.abs(brown).max()
amb=brown*env(0,5.6,att=.8,rel=.8)*.12
# discreet phone ring in the lobby
def ring():
    tt=np.arange(int(SR*.9))/SR; return (np.sin(2*np.pi*880*tt)+np.sin(2*np.pi*1100*tt))*(np.sin(2*np.pi*22*tt)>0)*np.exp(-tt*2)*np.minimum(1,tt*80)
add(ring(),1.0,.03,pan=.4); add(ring(),2.6,.025,pan=.4)
for k,s0 in enumerate((1.0,1.75,2.5,3.25)): add(np.sin(2*np.pi*(1400+120*k)*np.arange(int(SR*.12))/SR)*np.exp(-np.arange(int(SR*.12))/SR*30),s0,.06,pan=(-.4 if k%2 else .4))
L+=amb; R+=np.roll(amb,300)

# --- pluck arpeggio from 5 s (gold) ---
def pluck(f,dur=.9):
    tt=np.arange(int(SR*dur))/SR
    return (np.sin(2*np.pi*f*tt)+.3*np.sin(2*np.pi*2*f*tt)+.12*np.sin(2*np.pi*3.01*f*tt))*np.exp(-tt*5)
arp=[72,76,79,84,79,76]
bpm=110; beat=60/bpm; step=beat/2
x=5.3; i=0
while x<30.1:
    g=.05 if x<11 else (.065 if x<17 else .085)
    add(pluck(hz(arp[i%len(arp)]+(-3 if 17<=x<20.5 else 0))),x,g,pan=(-.4 if i%2 else .4))
    x+=step; i+=1

# --- pulse / kick from 11 s, hats from 17 s ---
def kick():
    tt=np.arange(int(SR*.45))/SR; f=45+80*np.exp(-tt*28)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*7)
def hat():
    n=rng.standard_normal(int(SR*.08)); n=np.diff(n,prepend=0); return n*np.exp(-np.arange(len(n))/SR*55)
x=11.0; b=0
while x<30.1:
    if x>=11: add(kick(),x,.32 if x<17 else .42)
    if x>=17: add(hat(),x+beat/2,.05,pan=.3)
    if x>=20.5: add(hat(),x+beat*.75,.03,pan=-.3)
    x+=beat; b+=1

# --- riser into reveal 21.5–24 ---
n=rng.standard_normal(N); n=np.diff(n,prepend=0)
ris=n*env(27.8,30.25,att=2.3,rel=.05)**2*.10
L+=ris; R+=np.roll(ris,120)

# --- notifications ---
def blip(f1,f2,d=.16):
    tt=np.arange(int(SR*d))/SR
    return (np.sin(2*np.pi*f1*tt)*(tt<d/2)+np.sin(2*np.pi*f2*tt)*(tt>=d/2))*np.exp(-tt*18)*np.minimum(1,tt*400)
add(blip(1250,1660),7.0,.16)        # message sent
add(blip(990,1320),8.0,.18)         # Alfred reply
add(blip(1250,1660),9.3,.13)        # quick reply 20h30
add(blip(1320,1760),9.95,.15)       # confirmed
for s0 in (17.3,17.65,18.0,18.35,18.7): add(blip(1500,1500,.08),s0,.05,pan=.2)  # dashboard feed
add(blip(1100,1470),19.6,.08)       # assigned to Spa
add(blip(880,1175),22.35,.08)       # task moved
add(blip(1320,1760),23.9,.09)       # opportunity booked
def tick(): tt=np.arange(int(SR*.03))/SR; return np.sin(2*np.pi*3000*tt)*np.exp(-tt*200)
for k in range(15): add(tick(),5.6+k*.085,.04)   # typing

# --- whoosh into Victoria + chime when she answers ---
wh=rng.standard_normal(int(SR*1.2)); wh=lp(wh,.08); tt=np.arange(len(wh))/SR
wh*=np.sin(np.pi*tt/1.2)**2; add(wh/np.abs(wh).max(),10.6,.22)
def bell(f,d=2.4):
    tt=np.arange(int(SR*d))/SR
    return sum(a*np.sin(2*np.pi*f*r*tt)*np.exp(-tt*dk) for r,a,dk in ((1,1,2.2),(2.76,.4,3.5),(5.4,.2,5),(8.9,.08,7)))
add(bell(hz(84)),14.8,.10,pan=-.2); add(bell(hz(91)),14.92,.07,pan=.2)


# --- montage card whooshes ---
for s in (17.0,18.6,21.0,23.5,25.0,25.95,26.9,27.85,28.8):
    w2=rng.standard_normal(int(SR*.35)); w2=np.diff(w2,prepend=0); tt=np.arange(len(w2))/SR
    add(w2*np.sin(np.pi*tt/.35)**2,s-.15,.035)

# --- reveal: impact at 24 (facade), logo shimmer 26.4 ---
def boom():
    tt=np.arange(int(SR*3))/SR; f=38+30*np.exp(-tt*6)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*1.4)
add(boom(),30.2,.5)
for k,m in enumerate([84,88,91,96]): add(bell(hz(m),3.0),32.0+k*.08,.05,pan=(-.3+.2*k))
add(blip(990,1320),33.5,.05)        # CTA

# --- voices: Lobbii voice (narration + Victoria) and the guest ---
import soundfile as sf
VOX=[("vo1",0.7,1.0,0),("vo2",5.55,1.0,0),("guest",11.7,.9,-.12),("vic",15.0,1.05,.08),("vo3",18.2,1.0,0),("vo4",25.3,1.0,0),("vo5",30.35,1.05,0)]
V=np.zeros(N)
for name,st,g,_ in VOX:
    x,sr=sf.read(f"voice/proc/{name}.wav"); assert sr==SR
    i=int(st*SR); n=min(len(x),N-i); V[i:i+n]+=x[:n]*g
V/=np.abs(V).max()
# envelope of voice presence -> smooth sidechain duck on music (-7 dB)
e=(np.abs(V)>0.02).astype(float)
k=np.ones(int(SR*.25))/int(SR*.25); e=np.clip(np.convolve(e,k,'same')*3,0,1)
e=np.convolve(e,np.ones(int(SR*.12))/int(SR*.12),'same')
duck=1-.55*e

# --- convolution reverb (FFT) ---
def reverb(x,secs=2.4,seed=3,damp=3.2):
    n=int(SR*secs); tt=np.arange(n)/SR
    ir=np.random.default_rng(seed).standard_normal(n)*np.exp(-tt*damp)
    ir=np.convolve(ir,np.ones(6)/6,'same')    # soften highs
    ir[:int(SR*.012)]=0; ir/=np.sqrt((ir**2).sum())
    m=len(x)+n-1; F=1<<int(np.ceil(np.log2(m)))
    return np.fft.irfft(np.fft.rfft(x,F)*np.fft.rfft(ir,F),F)[:len(x)]
mx=max(np.abs(L).max(),np.abs(R).max()); L/=mx; R/=mx
# warm the music bus: gentle high-shelf cut above 9 kHz
def tilt(x):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/(1+(f/9000)**2)**.25; return np.fft.irfft(X,len(x))
L,R=tilt(L),tilt(R)
L=L*duck+.22*reverb(L,seed=3); R=R*duck+.22*reverb(R,seed=4)
mL,mR=.62,.62
vL=V+.10*reverb(V,1.1,5,6); vR=V+.10*reverb(V,1.1,6,6)
L=L*mL+vL*.95; R=R*mR+vR*.95
fade=np.clip((D-t)/1.4,0,1); L*=fade; R*=fade
mx=max(np.abs(L).max(),np.abs(R).max())
L=np.tanh(L/mx*1.2)/np.tanh(1.2)*.89; R=np.tanh(R/mx*1.2)/np.tanh(1.2)*.89
pcm=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open('out/soundtrack.wav','wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
print('ok')
