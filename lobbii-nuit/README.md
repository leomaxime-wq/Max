# LOBBII — « 24 heures dans votre hôtel » · 30 s · 9:16

Troisième approche, plus cinématographique : une journée racontée heure par heure, de 3 h du matin à minuit. Le film suit de vrais moments de service plutôt qu'une liste de fonctionnalités, et se termine sur « Votre hôtel ne dort jamais. Lobbii non plus. »

| Fichier | Rôle |
|---|---|
| `LOBBII_24h_30s_9x16.mp4` | 1080×1920, 30 s, 60 fps, H.264 + AAC 256k (−14 LUFS) |
| `index.html` | Le film (ouvrir dans un navigateur pour le lire en boucle) |
| `render.mjs` / `audio.py` | `python3 audio.py && node render.mjs --dur 30 --fps 60` (`--scale 2` pour la 4K) |
| `voice/` | `gen_voices.py` (Kokoro) + voix brutes et traitées (`proc/`) |

## Déroulé

| Temps | Moment | À l'écran | Son / voix |
|---|---|---|---|
| 0–1,7 s | **03:12**, chambre 412 | Grande horloge sur noir | Note de piano, vagues lointaines |
| 1,2–7,4 s | Une cliente ne dort pas | WhatsApp en mode nuit : « Une tisane, ce serait possible ? » → Alfred : « Une camomille et un plaid vous sont montés dans dix minutes. » · ALFRED répond. Même à 3 heures du matin. | On frappe à la porte : la tisane arrive |
| 7–8,5 s | L'horloge défile jusqu'à **07:45** | | Tic-tac accéléré |
| 8,2–17,4 s | Suite 318, une cliente internationale | Interface Victoria, transcription anglaise + sous-titre français · VICTORIA — Elle répond dans la langue de chaque client. | Cliente (voix américaine) : « Victoria, could you book me a taxi to the airport? Around nine? » · Victoria (voix britannique) : « Of course. Your driver will be waiting for you at the entrance, at nine. » |
| 17,2–23 s | **11:30**, la direction | Tableau de bord « Depuis minuit » qui récapitule les demandes vues dans le film (tisane livrée à 03:24, taxi réservé…), équipes, opportunités · Centralisez. Anticipez. Pilotez. | Narratrice : « Pendant que vos équipes se concentrent sur l'essentiel, Lobbii s'occupe du reste. » |
| 22,6–25,6 s | **23:59**, façade de nuit | Les fenêtres s'allument · Votre hôtel ne dort jamais. | Narratrice : « Votre hôtel ne dort jamais. » |
| 25,2–30 s | Signature | Lobbii non plus. → LOBBII · L'intelligence au service de votre performance hôtelière · Demandez votre démonstration → · mylobbii.com | Narratrice : « Lobbii non plus. » |

## Voix

Voix neuronales open source (Kokoro). Les voix anglaises de Kokoro (af_heart, bf_emma) sont nettement plus naturelles que sa seule voix française (ff_siwis) : le film confie donc le dialogue à une cliente internationale. Cela montre aussi que Victoria parle la langue de chaque client.

Pour des voix vraiment humaines (comédiens, ou ElevenLabs), il suffit de remplacer les fichiers de `voice/proc/` (mêmes noms, mêmes textes, 48 kHz) puis de relancer `audio.py`. Les temps de départ sont dans `VOX` (`audio.py`) et `T_GUEST` / `T_VIC` (`index.html`).

## À remplacer avant publication

- Tableau de bord : maquette, à remplacer par des captures de la vraie interface Lobbii.
- Logo : mot-symbole provisoire (`#word`).
- Les données du tableau de bord sont fictives et ne contiennent aucun indicateur de performance ni témoignage.
