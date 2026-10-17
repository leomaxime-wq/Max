# Musique « feel good » pour la version pro : house / nu-disco élégante, 120 BPM, fa majeur.
# Progression Si♭maj7 – Do6/9 – Lam7 – Rém9 (2 s par mesure), basse disco en octaves,
# accords de piano électrique syncopés, clap sur 2 et 4, charleston ouvert sur les contretemps,
# mélodie à partir de 18 s, plein régime 30–43 s, break 43–49 s, accord final sur le logo à 49 s.
# -> $OUT/soundtrack.wav (-14 LUFS)
import numpy as np, wave, os, subprocess, json
OUT=os.environ.get('OUT','out'); os.makedirs(OUT,exist_ok=True)
SR=48000; D=55.0; N=int(SR*D); t=np.arange(N)/SR
rng=np.random.default_rng(3)
BPM=120; BEAT=60/BPM; BAR=4*BEAT
def hz(m): return 440*2**((m-69)/12)
def tt(d): return np.arange(int(SR*d))/SR
class Bus:
    def __init__(s): s.L=np.zeros(N); s.R=np.zeros(N)
    def add(s,sig,start,g=1.0,pan=0.0):
        i=int(round(start*SR)); n=min(len(sig),N-i)
        if n<=0 or i<0: return
        s.L[i:i+n]+=sig[:n]*g*(1-pan); s.R[i:i+n]+=sig[:n]*g*(1+pan)
def lowpass(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); return np.fft.irfft(X/np.sqrt(1+(f/fc)**4),len(x))
def highpass(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); return np.fft.irfft(X*(1-1/np.sqrt(1+(f/fc)**4)),len(x))
def noise(d): return rng.standard_normal(int(SR*d))

drums,bass,keys,pads,lead,fx=Bus(),Bus(),Bus(),Bus(),Bus(),Bus()

# ---------- harmonie ----------
PROG=[(46,[58,62,65,69]),(48,[60,64,67,74]),(45,[57,60,64,67]),(38,[57,60,65,64+12])]   # basse, accord
def chord_at(x): return PROG[int(x//BAR)%4]

# ---------- sons ----------
def kick():
    a=tt(.42); f=48+110*np.exp(-a*35)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-a*7.5)+.25*highpass(noise(.42),2500)*np.exp(-a*120)
def clap():
    n=highpass(noise(.3),1200); a=tt(.3)
    e=sum((a>=o)*np.exp(-np.maximum(a-o,0)*90) for o in (0,.011,.022))*.6+np.exp(-a*14)*(a>=.022)
    return lowpass(n,7000)*e
def hat(open_=False):
    d=.22 if open_ else .05; a=tt(d); return highpass(noise(d),7000)*np.exp(-a*(14 if open_ else 70))
def shaker():
    a=tt(.07); return highpass(noise(.07),5000)*np.sin(np.pi*a/.07)**2
def ep(m,d=.35,vel=1.0):   # piano électrique (type Rhodes)
    a=tt(d+.6); f=hz(m); env=np.exp(-a*2.2)*np.minimum(1,a*500)*np.where(a<d,1,np.exp(-(a-d)*14))
    s=np.sin(2*np.pi*f*a+.8*np.sin(2*np.pi*f*a)*np.exp(-a*6))+.25*np.sin(2*np.pi*2*f*a)+.12*np.sin(2*np.pi*7*f*a)*np.exp(-a*25)
    return s*env*(1+.12*np.sin(2*np.pi*5*a))*vel
def bassnote(m,d):
    a=tt(d); f=hz(m); s=sum(np.sin(2*np.pi*f*h*a)/h**1.3 for h in range(1,7))*.6+np.sin(2*np.pi*f*a)
    return s*np.minimum(1,a*400)*np.exp(-a*3)*np.clip((d-a)/.02,0,1)
def pluck(m,d=.4):
    a=tt(d+.3); f=hz(m)
    s=np.sin(2*np.pi*f*a)+.45*(2/np.pi)*np.arcsin(np.sin(2*np.pi*f*a))+.15*np.sin(2*np.pi*3*f*a)*np.exp(-a*12)
    return s*np.exp(-a*5)*np.minimum(1,a*800)
def padnote(m,d):
    a=tt(d); f=hz(m); s=np.zeros(len(a))
    for det in (-.006,-.002,.002,.006):
        s+=sum(np.sin(2*np.pi*f*(1+det)*h*a+h*det*900)/h**1.4 for h in range(1,6))
    return s*np.minimum(1,a/.6)*np.clip((d-a)/.8,0,1)

# ---------- arrangement ----------
def sec(x):
    if x<4: return 'intro'
    if x<8: return 'build'
    if x<18: return 'A'
    if x<30: return 'B'
    if x<43: return 'C'
    if x<49: return 'break'
    return 'end'
kicks=[]
b=0
while b*BEAT<D-1e-6:
    x=b*BEAT; s=sec(x); beat=b%4
    if s in('build','A','B','C') or (s=='end' and x<51):
        g={'build':.5,'A':.85,'B':.9,'C':1.0,'end':1.0}[s]; drums.add(kick(),x,g); kicks.append(x)
    if s in('A','B','C') and beat in(1,3): drums.add(clap(),x,.32 if s!='C' else .38,pan=.05)
    if s in('A','B','C'): drums.add(hat(True),x+BEAT/2,.10 if s=='A' else .13,pan=.25)
    if s in('B','C'):
        for k in (0,1,3): drums.add(shaker(),x+k*BEAT/4,.05+.03*(k==1),pan=-.3)
    if s=='C' and beat==0 and int(x//BAR)%2==0: drums.add(highpass(noise(1.4),5000)*np.exp(-tt(1.4)*3),x,.06,pan=.2)  # crash léger
    b+=1
# roulement avant 30 s et 43 s
for st,en in ((28.0,30.0),(41.0,43.0)):
    n=0;x=st
    while x<en-1e-6:
        k=(x-st)/(en-st); drums.add(clap(),x,.06+.22*k**2,pan=.1*np.sin(n)); x+=BEAT/(2 if k<.5 else 4); n+=1

# basse disco en octaves
x=8.0
while x<43-1e-6:
    r,_=chord_at(x); i=int(round(x/(BEAT/2)))
    m=r if i%2==0 else r+12
    if not(i%8==0 and False): bass.add(bassnote(m,BEAT/2*.85),x,.55 if i%2==0 else .42)
    x+=BEAT/2
# basse du final
bass.add(bassnote(41,3.5),49.0,.7); bass.add(bassnote(29,3.5),49.0,.5)

# accords : nappes longues + piano électrique syncopé
for bar in range(int(D//BAR)+1):
    x=bar*BAR; s=sec(x); r,ch=chord_at(x)
    if x>=D: break
    if s in('intro','build','break','B','C'):
        for m in ch: pads.add(highpass(padnote(m,BAR+.6),180),x,.03 if s in('B','C') else .06)
    if s in('A','B','C'):
        for off,v in ((0,.8),(1.5*BEAT,1.0),(2.5*BEAT,.75),(3.5*BEAT,.9)):
            for m in ch: keys.add(ep(m,.22,v),x+off,.06,pan=-.15)
    if s in('intro','build','break'):
        for k,m in enumerate(ch): keys.add(ep(m,1.6,.9),x+k*.03,.07,pan=.1)
# accord final (logo) : Fa maj9
for k,m in enumerate([53,57,60,64,67,72]): keys.add(ep(m,3.5,1.0),49.0+k*.025,.09); pads.add(padnote(m,6),49.0,.06)

# mélodie (fa pentatonique) à partir de 18 s
HOOK=[(0,69,.5),(.5,72,.5),(1,74,.5),(1.5,72,.25),(2,69,.5),(3,67,.5),(3.5,65,.5),
      (4,67,.5),(4.5,69,.5),(5,72,1),(6,74,.5),(6.5,77,.5),(7,76,1)]
for start,end,g,octv in ((18,30,.10,0),(30,43,.12,12),(43,49,.07,0)):
    x0=start
    while x0<end-1e-6:
        for bt,m,d in HOOK:
            x=x0+bt*BEAT
            if x<end: lead.add(pluck(m+octv,d*BEAT),x,g,pan=.2); lead.add(pluck(m+octv,d*BEAT),x+3*BEAT/4,g*.3,pan=-.35)  # écho
        x0+=8*BEAT

# montées & impacts
def riser(a,b,g):
    d=b-a; n=highpass(noise(d),800); s=tt(d); fx.add(n*(s/d)**2.5,a,g)
riser(6.0,8.0,.06); riser(16.0,18.0,.05); riser(28.0,30.0,.07); riser(46.5,49.0,.08)
def boom(d=3.5):
    a=tt(d); f=36+50*np.exp(-a*6); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-a*1.3)
fx.add(boom(),8.0,.35); fx.add(boom(),30.0,.35); fx.add(boom(5),49.0,.55)

# ---------- mixage : sidechain (pompe house), réverbe, bus ----------
sc=np.ones(N)
for k in kicks:
    i=int(k*SR); n=min(int(SR*BEAT),N-i); a=np.arange(n)/SR; sc[i:i+n]=np.minimum(sc[i:i+n],1-.55*np.exp(-a/.09))
def reverb(x,secs=2.2,seed=1,damp=3.0):
    n=int(SR*secs); a=np.arange(n)/SR; ir=np.random.default_rng(seed).standard_normal(n)*np.exp(-a*damp)
    ir=np.convolve(ir,np.ones(10)/10,'same'); ir[:int(SR*.02)]=0; ir/=np.sqrt((ir**2).sum())
    F=1<<int(np.ceil(np.log2(len(x)+n))); return np.fft.irfft(np.fft.rfft(x,F)*np.fft.rfft(ir,F),F)[:len(x)]
intro_lp=np.interp(t,[0,7.9,8.0,43,43.01,48.8,49],[1,1,0,0,1,1,0])        # filtre passe-bas sur l'intro et le break
L=np.zeros(N); Rr=np.zeros(N)
for bus,g,duck,rv in ((drums,1.0,False,.05),(bass,.9,True,0),(keys,1.0,True,.18),(pads,1.0,True,.3),(lead,1.0,True,.25),(fx,1.0,False,.2)):
    for ch,acc in ((bus.L,0),(bus.R,1)):
        y=ch*g*(sc if duck else 1)
        if rv: y=y+rv*reverb(y,seed=acc+3)
        y=y*(1-intro_lp)+lowpass(y,900)*intro_lp if bus in(keys,pads,drums,lead) else y
        if acc==0: L+=y
        else: Rr+=y
L=highpass(L,28); Rr=highpass(Rr,28)
def air(x):   # +3 dB au-dessus de 6 kHz, -2 dB vers 300 Hz : mix plus clair
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR)
    X*=1+.41/(1+(6000/np.maximum(f,1))**2)-.2*np.exp(-((np.log2(np.maximum(f,1)/300))**2)/.5); return np.fft.irfft(X,len(x))
L,Rr=air(L),air(Rr)
fade=np.clip((D-t)/2.5,0,1)**1.3*np.clip(t/.3,0,1); L*=fade; Rr*=fade
mx=max(np.abs(L).max(),np.abs(Rr).max()); L=np.tanh(L/mx*1.6)/np.tanh(1.6)*.9; Rr=np.tanh(Rr/mx*1.6)/np.tanh(1.6)*.9
pcm=(np.stack([L,Rr],1)*32767).astype('<i2')
with wave.open(f'{OUT}/soundtrack_raw.wav','wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
m=subprocess.run(['ffmpeg','-hide_banner','-i',f'{OUT}/soundtrack_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=20:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
j=json.loads(m[m.rindex('{'):m.rindex('}')+1])
af=f"loudnorm=I=-14:TP=-1.5:LRA=20:linear=true:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}"
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{OUT}/soundtrack_raw.wav','-af',af,'-ar','48000',f'{OUT}/soundtrack.wav'],check=True)
print('ok')
