# LOBBII — Trailer B2B « Votre hôtel ne dort jamais. Lobbii non plus. » · 35 s · 9:16

Cible : directeurs généraux, directeurs des opérations, responsables hébergement, groupes hôteliers.

| Fichier | Rôle |
|---|---|
| `LOBBII_B2B_9x16.mp4` | 1080×1920, 60 fps, H.264 + AAC 256k (−14 LUFS), avec voix |
| `index.html` | Le film (ouvrir dans un navigateur pour le lire en boucle) |
| `render.mjs` / `audio.py` | Rendu image et son (`python3 audio.py && node render.mjs --dur 35 --fps 60`, `--scale 2` pour la 4K) |
| `voice/` | Voix générées (`gen_voices.py`, modèle Kokoro, voix française ff_siwis) et versions traitées (`proc/`) |

## Minutage

| Temps | Séquence | Texte à l'écran |
|---|---|---|
| 0–5 s | Lobby, réception sollicitée, demandes qui arrivent à toute heure (horloge 07:42 → 02:14) | Vos clients ont des attentes. / À chaque instant. |
| 5–11 s | WhatsApp : demande de table → Alfred répond → choix 20h30 en un tap → confirmation, restaurant prévenu | ALFRED — L'assistant IA disponible 24h/24. |
| 11–17 s | Suite vue mer, interface vocale Victoria (forme d'onde + transcription) | VICTORIA — L'intelligence devient conversation. |
| 17–25 s | Tableau de bord Lobbii sur portable : demandes en direct, historique de conversation, tâches des équipes, opportunités, demandes par service | Centralisez vos échanges. / Fluidifiez vos opérations. / Valorisez chaque opportunité. |
| 25–30 s | Spa, restaurant, room service, client détendu, équipe de réception (dessins au trait dorés) | Une meilleure expérience client. / Des équipes plus efficaces. / De nouvelles opportunités de revenus. |
| 30–35 s | Fond crème : accroche, logo, signature, appel à l'action | Votre hôtel ne dort jamais. Lobbii non plus. → LOBBII · L'intelligence au service de votre performance hôtelière. · Alfred • Victoria • Une plateforme intelligente · [Demandez votre démonstration →] · mylobbii.com |

## Éléments à remplacer avant publication

- **Interface Lobbii** : le tableau de bord (17–25 s) est une maquette fidèle au brief. Remplacez-la par des captures de la vraie plateforme (ou fournissez-les pour que je reconstruise l'écran à l'identique).
- **Logo officiel** : le mot-symbole « LOBBII » est provisoire (`#word` dans `index.html`).
- **Musique** : maquette synthétisée calée sur les repères (pulsation dès 11 s, montée 27,8–30,2 s, impact 30,2 s). À remplacer par une piste sous licence.
- **Données affichées** : les compteurs du tableau de bord (12 demandes, 64 conversations…) sont des données d'interface fictives, sans indicateur de performance ni promesse chiffrée, et le film ne contient aucun témoignage client.

## Voix

Une seule voix incarne Lobbii : elle raconte le film et répond en tant que Victoria. La cliente a une voix distincte, plus grave. La musique s'efface automatiquement sous chaque phrase.

| Temps | Voix | Texte |
|---|---|---|
| 0,7 s | Lobbii | Vos clients ont des attentes. À chaque instant. |
| 5,6 s | Lobbii | Alfred leur répond sur WhatsApp. Immédiatement. À toute heure. |
| 11,7 s | Cliente | Victoria, peux-tu m'aider à organiser un massage demain ? |
| 15,0 s | Victoria | Bien sûr. Je vais vous aider. |
| 18,2 s | Lobbii | Pour vos équipes, tout est centralisé. Chaque demande. Chaque tâche. Chaque opportunité. |
| 25,3 s | Lobbii | Une expérience plus fluide. Des équipes plus efficaces. De nouveaux revenus. |
| 30,35 s | Lobbii | Votre hôtel ne dort jamais. Lobbii non plus. |

Ce sont des voix de synthèse neuronales open source (Kokoro). Pour la diffusion officielle, une comédienne ou une voix ElevenLabs sur le même texte et le même minutage donnera un rendu encore plus haut de gamme : remplacez les fichiers de `voice/proc/` puis relancez `audio.py`.
