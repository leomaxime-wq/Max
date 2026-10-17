# Bande-son de synthèse du film RESTO CONSEIL (55 s, 120 BPM) -> out/soundtrack.wav
# Musique électronique cinématographique : nappes, basse profonde, pulsation, montée, ralentissement final
# + design sonore : salle, verres, vagues, crayon, porcelaine, cuisine, murmure de salle.
import numpy as np, wave, os
PHOTO=os.environ.get('PHOTO')=='1'   # version photographique : pas de bruitages de cuisine / verres / vagues
OUT=os.environ.get('OUT','out')
SR=48000; D=55.0; N=int(SR*D); t=np.arange(N)/SR
rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N)
BPM=120; BEAT=60/BPM
def hz(m): return 440*2**((m-69)/12)
def add(sig,start,g=1.0,pan=0.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*g*(1-pan); R[i:i+n]+=sig[:n]*g*(1+pan)
def env(a,b,att=.05,rel=.3): return np.clip((t-a)/att,0,1)*np.clip((b-t)/rel,0,1)
def bandpass(x,lo,hi):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=((f>=lo)&(f<=hi)); return np.fft.irfft(X,len(x))
def lowpass(x,fc,order=2):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/np.sqrt(1+(f/fc)**(2*order)); return np.fft.irfft(X,len(x))
def noise(sec): return rng.standard_normal(int(SR*sec))

# ---------- nappes (pad) ----------
chords=[(0,[50,57,62,65,69]),(4,[46,53,62,65,70]),(8,[50,57,62,65,69]),(12,[43,50,58,62,67]),(16,[45,52,61,64,69]),
        (18,[50,57,62,65,69]),(22,[46,53,62,65,70]),(26,[43,55,58,62,67]),(28,[45,52,61,64,69]),
        (30,[50,57,62,65,69,74]),(33.5,[46,58,62,65,70]),(37,[43,55,62,67,70]),(40,[45,57,61,64,69,73]),
        (43,[50,57,62,65,69,74]),(46.5,[46,53,62,65,70]),(49,[50,57,62,66,69,74])]
pad=np.zeros((2,N))
for k,(st,notes) in enumerate(chords):
    en=chords[k+1][0] if k+1<len(chords) else D
    e=env(st-.25,en+.8,att=.9,rel=1.0)
    for m in notes:
        f=hz(m)
        for ch,det in ((0,-.003),(1,.003)):
            pad[ch]+=sum(np.sin(2*np.pi*f*(1+det)*h*t+h*1.3)/h**1.7 for h in (1,2,3,4,5))*e
swell=.45+.55*np.clip(t/30,0,1)
pad*=.032*swell
L+=pad[0]; R+=pad[1]

# ---------- basse profonde ----------
def bassnote(f,d):
    tt=np.arange(int(SR*d))/SR
    s=np.sin(2*np.pi*f*tt)+.35*np.sin(2*np.pi*2*f*tt)+.12*np.sin(2*np.pi*3*f*tt)
    return s*np.minimum(1,tt*60)*np.exp(-tt*1.6)
roots={0:38,4:34,8:38,12:31,16:33,18:38,22:34,26:31,28:33,30:38,33.5:34,37:31,40:33}
def root_at(x):
    r=38
    for k in sorted(roots):
        if x>=k: r=roots[k]
    return r
# drone in S1, 8ths from 18 s
add(lowpass(np.sin(2*np.pi*hz(26)*t)*env(0,8.3,2.5,.6),200),0,.11)
x=8.0
while x<43-1e-6:
    step=BEAT if x<18 else BEAT/2
    g=.16 if x<18 else (.2 if x<30 else .24)
    add(bassnote(hz(root_at(x)),step*1.6),x,g)
    x+=step

# ---------- percussions ----------
def kick(g=1):
    tt=np.arange(int(SR*.5))/SR; f=42+95*np.exp(-tt*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*6.5)*g
def hat(d=.07):
    n=np.diff(noise(d),prepend=0); return n*np.exp(-np.arange(len(n))/SR*60)
def clap():
    n=bandpass(noise(.25),900,5000); tt=np.arange(len(n))/SR
    e=sum(np.exp(-np.maximum(tt-o,0)*80)*(tt>=o) for o in (0,.012,.024))*np.exp(-tt*10); return n*e
def tick():
    tt=np.arange(int(SR*.03))/SR; return np.sin(2*np.pi*2400*tt)*np.exp(-tt*180)
x=8.0; b=0
while x<43-1e-6:
    add(kick(),x,.30 if x<18 else (.38 if x<30 else .44))
    if x>=8:  add(tick(),x+BEAT/2,.035,pan=.3*(1 if b%2 else -1))
    if x>=18: add(hat(),x+BEAT/2,.05,pan=.25); add(hat(.04),x+BEAT*.75,.025,pan=-.25)
    if x>=30 and b%2==1: add(clap(),x,.07)
    x+=BEAT; b+=1

# ---------- arpège (or) ----------
def pluck(f,d=.8):
    tt=np.arange(int(SR*d))/SR
    return (np.sin(2*np.pi*f*tt)+.3*np.sin(2*np.pi*2*f*tt)+.1*np.sin(2*np.pi*3.01*f*tt))*np.exp(-tt*6)*np.minimum(1,tt*300)
arp=[0,7,12,15,12,7,3,7]
x=8.0;i=0
while x<43-1e-6:
    r=root_at(x)+36; g=.035 if x<18 else (.045 if x<30 else .06)
    add(pluck(hz(r+arp[i%8])),x,g,pan=(-.45 if i%2 else .45))
    x+=BEAT/2 if x<30 else BEAT/4; i+=1

# ---------- montées & impacts ----------
def riser(a,b,g):
    n=bandpass(noise(b-a),400,9000); tt=np.arange(len(n))/SR; e=(tt/(b-a))**2.2
    tone=np.sin(2*np.pi*np.cumsum(200+1400*(tt/(b-a))**2)/SR)*.25
    add((n+tone)*e,a,g)
riser(6.6,8.0,.05); riser(16.6,18.0,.05); riser(28.6,30.0,.06); riser(41.0,43.0,.09)
def boom(d=4,g=1):
    tt=np.arange(int(SR*d))/SR; f=34+40*np.exp(-tt*5)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*1.1)*g
add(boom(),8.0,.35); add(boom(),18.0,.35); add(boom(),30.0,.42); add(boom(5),43.0,.55); add(boom(6),49.0,.6)
for c in ((10,12,14,22,25.5,27,31,34.3,38.6) if PHOTO else (10,12,14,16,20,22,24,26,28,31.5,33,34.5,36,37.5,39,41)):   # souffles de coupe
    w=bandpass(noise(.4),600,7000); tt=np.arange(len(w))/SR; add(w*np.sin(np.pi*tt/.4)**2,c-.2,.03,pan=.3*np.sin(c))

# ---------- final : ralentissement, piano, cloches ----------
def piano(f,d=3.5):
    tt=np.arange(int(SR*d))/SR
    return sum(a*np.sin(2*np.pi*f*h*tt)*np.exp(-tt*(1.2+h*.8)) for h,a in ((1,1),(2,.45),(3,.2),(4,.1)))*np.minimum(1,tt*400)
for k,(st,m) in enumerate([(43.2,74),(44.4,72),(45.6,69),(46.8,70),(48.0,69),(49.6,74),(50.8,78),(52.0,81)]):
    add(piano(hz(m)),st,.07,pan=(-.2 if k%2 else .2))
def bell(f,d=3.0):
    tt=np.arange(int(SR*d))/SR
    return sum(a*np.sin(2*np.pi*f*r*tt)*np.exp(-tt*dk) for r,a,dk in ((1,1,1.6),(2.76,.4,3),(5.4,.2,5)))
for k,m in enumerate([86,90,93,98]): add(bell(hz(m)),49.25+k*.09,.035,pan=-.3+.2*k)

# ---------- design sonore ----------
room=lowpass(noise(D),500); room/=np.abs(room).max()
L+=room*.05*env(0,8.4,1,.6); R+=np.roll(room,700)*.05*env(0,8.4,1,.6)
def clink(f=2900,d=1.6):
    tt=np.arange(int(SR*d))/SR
    return sum(a*np.sin(2*np.pi*f*r*tt)*np.exp(-tt*dk) for r,a,dk in ((1,1,4),(1.51,.6,5),(2.43,.35,7),(3.1,.2,9)))*np.minimum(1,tt*2000)
if not PHOTO: add(clink(3100),1.3,.05,pan=.4); add(clink(2600),2.4,.035,pan=-.3)
waves=lowpass(noise(3.4),900); tt=np.arange(len(waves))/SR; waves*=(.5+.5*np.sin(2*np.pi*tt/2.6-1.5))**2
if not PHOTO: add(waves/np.abs(waves).max(),5.2,.12)
for k in range(0 if PHOTO else 10):                   # crayon sur papier (plans)
    s=bandpass(noise(.12+.1*rng.random()),2500,9000); s*=np.hanning(len(s)); add(s,8.25+k*.17,.05,pan=.2)
p2=bandpass(noise(.5),300,4000); 0 if PHOTO else add(p2*np.hanning(len(p2)),12.05,.06)          # carte posée
for st in () if PHOTO else (14.6,14.85,15.1,15.6,16.2,16.5,16.8,17.1,17.4):                     # porcelaine / pince
    add(clink(4200+rng.random()*900,.35),st,.02,pan=.15)
siz=bandpass(noise(4.2),2500,12000); siz*=.6+.4*np.abs(np.sin(np.arange(len(siz))/SR*9))
0 if PHOTO else add(siz*np.minimum(1,np.arange(len(siz))/SR*8)*np.clip((4.2-np.arange(len(siz))/SR)/.4,0,1),18.0,.05,pan=-.15)   # cuisine
for st in (() if PHOTO else (18.6,19.5,20.8,21.4)): add(clink(1700+rng.random()*400,.5),st,.03,pan=.3)                           # casseroles
mur=bandpass(noise(10),250,1600); m_e=.6+.4*lowpass(rng.standard_normal(len(mur)),3)/0.3
mur*=np.clip(m_e,0,1.4); mur/=np.abs(mur).max()
0 if PHOTO else add(mur*np.minimum(1,np.arange(len(mur))/SR)*np.clip((10-np.arange(len(mur))/SR)/1,0,1),22.0,.06)            # salle animée
0 if PHOTO else add(mur[:int(SR*6)]*np.hanning(int(SR*6)),36.5,.04)
if not PHOTO: add(clink(3000,2.2),42.55,.16); add(clink(3350,2.0),42.565,.12,pan=.2)       # les flûtes trinquent

# ---------- mixage ----------
def reverb(x,secs=2.6,seed=3,damp=2.6):
    n=int(SR*secs); tt=np.arange(n)/SR
    ir=np.random.default_rng(seed).standard_normal(n)*np.exp(-tt*damp); ir=np.convolve(ir,np.ones(8)/8,'same')
    ir[:int(SR*.015)]=0; ir/=np.sqrt((ir**2).sum())
    m=len(x)+n-1; F=1<<int(np.ceil(np.log2(m)))
    return np.fft.irfft(np.fft.rfft(x,F)*np.fft.rfft(ir,F),F)[:len(x)]
L=L+.25*reverb(L,seed=3); R=R+.25*reverb(R,seed=4)
L,R=lowpass(L,14000,1),lowpass(R,14000,1)
fade=np.clip((D-t)/2.0,0,1)**1.5*np.interp(t,[0,8,18,30,43,55],[.5,.65,.82,1,.9,.9]); L*=fade; R*=fade
mx=max(np.abs(L).max(),np.abs(R).max()); L=np.tanh(L/mx*1.3)/np.tanh(1.3)*.9; R=np.tanh(R/mx*1.3)/np.tanh(1.3)*.9
os.makedirs(OUT,exist_ok=True)
pcm=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open(f'{OUT}/soundtrack_raw.wav','wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
# normalisation -14 LUFS en deux passes, mode linéaire (préserve le crescendo)
import subprocess, json
m=subprocess.run(['ffmpeg','-hide_banner','-i',f'{OUT}/soundtrack_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=20:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
j=json.loads(m[m.rindex('{'):m.rindex('}')+1])
af=f"loudnorm=I=-14:TP=-1.5:LRA=20:linear=true:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}"
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{OUT}/soundtrack_raw.wav','-af',af,'-ar','48000',f'{OUT}/soundtrack.wav'],check=True)
print('ok')
