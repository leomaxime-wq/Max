# LOBBII — The Future of Hospitality · Trailer 30 s (9:16)

## Ce qui est livré

| Fichier | Rôle |
|---|---|
| `LOBBII_trailer_9x16.mp4` | Master 1080×1920, 30 fps, H.264 CRF 16 + AAC 256k (−15 LUFS) |
| `LOBBII_trailer_9x16_web.mp4` | Version légère (21 Mo) pour Reels / LinkedIn |
| `index.html` | Le film en motion design. Ouvrir dans un navigateur le lit en boucle. |
| `render.mjs` | Rendu image par image → MP4 (`node render.mjs`; `--scale 2` = 4K 2160×3840) |
| `audio.py` | Musique et sound design synthétisés → `out/soundtrack.wav` |

Pour refaire le rendu : `python3 audio.py && node render.mjs && ffmpeg -i out/video_noaudio.mp4 -i out/soundtrack.wav -c:v copy -c:a aac -b:a 256k -shortest LOBBII_trailer_9x16.mp4`

## Limites de cette version

- **Pas d’images photoréalistes.** Les décors (lobby, suite vue mer, terrasse, façade) sont des illustrations vectorielles. Les interfaces (WhatsApp, dashboard Lobbii) sont nettes et lisibles. Pour une version tournée ou générée par IA, voir la section suivante.
- **Pas de voix de Victoria.** Il y a un blanc de 14,2 à 16,0 s (musique baissée, carillon, sous-titre doré, forme d’onde). Il faut placer la voix enregistrée ou une voix de synthèse premium (ElevenLabs, par ex.) à 14,2 s.
- **Le logo est provisoire.** C’est un wordmark « LOBBII » en Inter Display Light. Pour mettre le vrai logo, remplacez `<div class="word" id="word">` dans `index.html` par le SVG officiel.
- **Musique synthétisée.** Elle sert de maquette pour le rythme (110 BPM, montée à partir de 11 s, impact à 24 s). Remplacez-la par une piste sous licence (Artlist, Musicbed) calée sur ces repères.

## Minutage

| Temps | Séquence | Texte à l’écran |
|---|---|---|
| 0–5 s | Lobby, lumière du matin, cliente qui arrive | L’hospitalité entre dans une nouvelle ère. |
| 5–11 s | WhatsApp avec Alfred : saisie → « écrit… » → proposition → Confirmer → « C’est réservé ✓ » | Alfred. Votre conciergerie intelligente, 24h/24. |
| 11–17 s | Suite vue mer, échange vocal avec Victoria, forme d’onde dorée | Victoria. L’hospitalité prend la parole. |
| 17–24 s | Montage : restaurant · room service · spa · dashboard réception · transmission à l’équipe · client satisfait | Une expérience personnalisée. / Des équipes connectées. / Chaque opportunité valorisée. |
| 24–30 s | Façade de nuit qui s’illumine → fond crème → logo, signature, canaux, URL | L’intelligence au service de l’hospitalité. · WhatsApp • Intelligence artificielle • Voice AI · mylobbii.com |

## Prompts pour la version photoréaliste (Veo / Sora / Runway / Kling)

Ces prompts servent à générer les plans réels. Les incrustations UI et les textes de ce projet se posent ensuite par-dessus au montage. Conseil : générez les plans sans texte ni écran lisible, puis ajoutez les interfaces au compositing pour qu’elles restent nettes.

**Style commun (à ajouter à chaque prompt) :** *vertical 9:16, photorealistic, shot on ARRI Alexa 35, 35mm anamorphic look, soft natural morning light, warm cream and off-white palette with deep black and subtle brushed-gold accents, refined contemporary luxury hotel architecture, slow fluid camera movement, shallow depth of field, subtle film grain, no text, no logos, no robots, no holograms, no futuristic effects.*

1. **Lobby (0–5 s).** Slow dolly-in through a grand five-star hotel lobby with tall cream travertine arches, morning sunlight streaming in diagonal beams, polished marble floor reflections. An elegant woman in her 30s in a camel coat walks in with a small leather bag; a receptionist behind a dark walnut desk with a thin brass edge greets her with a warm smile.
2. **Smartphone (5–11 s).** Macro close-up of a woman’s hand holding a modern smartphone, warm bokeh of a hotel bar at dusk behind. Screen as a neutral green/chroma placeholder (UI added in post). Gentle rack focus from the hand to the screen.
3. **Suite (11–17 s).** Wide shot of a luxury suite with floor-to-ceiling windows overlooking a calm Mediterranean sea, sheer linen curtains moving slightly in the breeze. The same woman sits on the edge of a white bed and speaks naturally, relaxed, as if talking to the room. Slow lateral slide.
4. **Montage (17–24 s), 6 plans d’environ 1 s chacun :** (a) a waiter places a refined plate on a candlelit seaside terrace table; (b) a room-service trolley with croissants and fresh juice enters a sunlit suite; (c) close-up of warm stones and eucalyptus in a minimalist spa cabin; (d) a receptionist glances at a slim tablet at the front desk (screen as a placeholder); (e) a spa therapist checks her phone and nods, then walks down a corridor; (f) the guest raises a glass of champagne on a terrace at golden hour, smiling.
5. **Révélation (24–26 s).** Aerial drone pull-back from a contemporary luxury seafront hotel at blue hour, windows lighting up one by one, then a smooth fade to a flat cream background.

**Voix de Victoria :** voix féminine, française, 30–40 ans, timbre chaud, débit posé, souriante. Texte : « Bien sûr. Je m’en occupe pour vous. » Ajoutez une légère reverb de pièce, sans effet robotique.
