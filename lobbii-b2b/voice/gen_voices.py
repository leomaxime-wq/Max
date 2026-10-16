import soundfile as sf, numpy as np, json, sys
from kokoro_onnx import Kokoro
k=Kokoro("kokoro-v1.0.onnx","voices-v1.0.bin")
out=sys.argv[1]
LINES={
 "vo1":("Vos clients ont des attentes. À chaque instant.",0.92),
 "vo2":("Alfred leur répond sur Ouatsape. Immédiatement. À toute heure.",0.95),
 "guest":("Victoria, peux-tu m'aider à organiser un massage demain ?",1.0),
 "vic":("Bien sûr. Je vais vous aider.",0.93),
 "vo3":("Pour vos équipes, tout est centralisé. Chaque demande. Chaque tâche. Chaque opportunité.",0.97),
 "vo4":("Une expérience plus fluide. Des équipes plus efficaces. De nouveaux revenus.",0.98),
 "vo5":("Votre hôtel ne dort jamais. Lobbii non plus.",0.98),
}
d={}
for name,(txt,sp) in LINES.items():
    s,sr=k.create(txt,voice="ff_siwis",speed=sp,lang="fr-fr")
    # trim silence
    a=np.abs(s); idx=np.where(a>0.01)[0]; s=s[max(0,idx[0]-240):idx[-1]+2400]
    sf.write(f"{out}/{name}.wav",s,sr); d[name]=round(len(s)/sr,2)
print(json.dumps(d))
