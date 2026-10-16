# Generates the film's voices with ElevenLabs (eleven_multilingual_v2).
# Needs ELEVENLABS_API_KEY in the environment and api.elevenlabs.io allowed by the network policy.
# Usage: python3 voice/gen_elevenlabs.py   (run from lobbii-nuit/) -> voice/<name>.wav, then processed by run_voices.sh
import json, os, subprocess, sys, urllib.request

KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("ELEVENLABS_API_KEY is not set")

# Premade ElevenLabs voices; override with env vars to use voices from your own library.
VOICES = {
    "guest": os.environ.get("EL_VOICE_GUEST", "EXAVITQu4vr4xnSDxMaL"),     # Sarah: American, soft
    "vic":   os.environ.get("EL_VOICE_VICTORIA", "Xb7hH8MSUJpSbSDYk0k2"),  # Alice: British, warm
    "vo":    os.environ.get("EL_VOICE_NARRATOR", "XB0fDUnXU5powFXDhCwa"),  # Charlotte: narrator (French via multilingual v2)
}
LINES = {
    "guest": ("guest", "Victoria, could you book me a taxi to the airport? ... Around nine?", 0.45),
    "vic":   ("vic",   "Of course. Your driver will be waiting for you at the entrance, at nine.", 0.6),
    "vo1":   ("vo",    "Pendant que vos équipes se concentrent sur l'essentiel… Lobbii s'occupe du reste.", 0.6),
    "vo2":   ("vo",    "Votre hôtel ne dort jamais.", 0.6),
    "vo3":   ("vo",    "Lobbii non plus.", 0.6),
}

here = os.path.dirname(os.path.abspath(__file__))
durations = {}
for name, (who, text, stability) in LINES.items():
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[who]}?output_format=mp3_44100_192",
        data=json.dumps({
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": stability, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True},
        }).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    )
    mp3 = os.path.join(here, f"{name}.mp3")
    with urllib.request.urlopen(req, timeout=120) as r, open(mp3, "wb") as f:
        f.write(r.read())
    wav = os.path.join(here, f"{name}.wav")
    # trim leading/trailing silence, 48 kHz mono
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.05",
                    "-ar", "48000", "-ac", "1", wav], check=True)
    os.remove(mp3)
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True)
    durations[name] = round(float(out.stdout), 2)
print(json.dumps(durations))
