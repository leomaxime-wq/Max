# Generates the film's voices with Kokoro (kokoro-onnx). Usage: python3 gen_voices.py <model_dir> <out_dir>
import soundfile as sf, numpy as np, json, sys
from kokoro_onnx import Kokoro
md,out=sys.argv[1],sys.argv[2]
k=Kokoro(f"{md}/kokoro-v1.0.onnx",f"{md}/voices-v1.0.bin")
# name: [(text, voice, lang, speed, pause_after_s), ...]  -> phrases joined with natural pauses
LINES={
 "guest":[("Victoria, could you book me a taxi to the airport?",  "af_heart","en-us",0.95,0.18),("Around nine?","af_heart","en-us",0.92,0)],
 "vic":  [("Of course.","bf_emma","en-gb",0.92,0.22),("Your driver will be waiting for you at the entrance, at nine.","bf_emma","en-gb",0.96,0)],
 "vo1":  [("Pendant que vos équipes se concentrent sur l'essentiel,","ff_siwis","fr-fr",0.93,0.25),("Lobbii s'occupe du reste.","ff_siwis","fr-fr",0.9,0)],
 "vo2":  [("Votre hôtel ne dort jamais.","ff_siwis","fr-fr",0.9,0)],
 "vo3":  [("Lobbii non plus.","ff_siwis","fr-fr",0.88,0)],
}
def trim(s):
    a=np.abs(s); i=np.where(a>0.01)[0]; return s[max(0,i[0]-240):i[-1]+1200]
d={}
for name,parts in LINES.items():
    chunks=[]
    for txt,v,lang,sp,p in parts:
        s,sr=k.create(txt,voice=v,speed=sp,lang=lang); chunks+= [trim(s),np.zeros(int(sr*p))]
    s=np.concatenate(chunks); sf.write(f"{out}/{name}.wav",s,sr); d[name]=round(len(s)/sr,2)
print(json.dumps(d))
