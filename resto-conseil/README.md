# RESTO CONSEIL — Film de marque · 55 s

Trailer en motion design cinématographique (silhouettes, lumière dorée, typographie éditoriale). Il n'y a ni visage, ni plat généré par IA, ni logo de partenaire.

## Livrables

| Fichier | Format | Usage |
|---|---|---|
| `RESTO_CONSEIL_55s_9x16.mp4` | 1080×1920 | Instagram Reels |
| `RESTO_CONSEIL_55s_4x5.mp4` | 1080×1350 | LinkedIn |
| `RESTO_CONSEIL_55s_16x9.mp4` | 1920×1080 | Site internet |

Caractéristiques : 30 i/s, H.264 et AAC 256 kb/s. L'audio est normalisé à −14 LUFS (norme des réseaux sociaux). Le film suit un crescendo de −26 dB à l'ouverture jusqu'au plein régime à 30 s.

Le film est un fichier unique, `index.html`, qui s'adapte aux trois formats. Pour le prévisualiser en boucle, ouvrez `index.html?f=916`, `?f=45` ou `?f=169` dans un navigateur.

Pour le recalculer :

```
python3 audio.py                         # bande-son -> out/soundtrack.wav
node render.mjs --f 916                  # images -> out/video_916.mp4 (idem 45, 169)
node render.mjs --f 169 --scale 2        # 16:9 en 4K (3840×2160)
ffmpeg -i out/video_916.mp4 -i out/soundtrack.wav -c:v copy -c:a aac -b:a 256k -shortest RESTO_CONSEIL_55s_9x16.mp4
```

## Découpage

| Temps | Séquence | Images | Texte à l'écran |
|---|---|---|---|
| 0–8 s | **L'expérience** | Salle de restaurant face à la mer au coucher du soleil (travelling avant), façade de palace au crépuscule, restaurant de plage méditerranéen | *Chaque lieu raconte une histoire.* / *Chaque concept commence par une vision.* |
| 8–18 s | **La création** | Plan d'architecte qui se dessine, planche de matières (marbre, noyer, laiton, lin, terre cuite, velours), carte annotée « signature », dressage d'une assiette à la pince | IMAGINER. CRÉER. DIFFÉRENCIER. (un mot par coupe) |
| 18–30 s | **L'expertise** | Cuisine en plein service, chef exécutif face à sa brigade, service en salle de palace, restaurant de destination animé, table de travail (concepts, carte, plan), tableau de pilotage | STRATÉGIE. EXPERTISE. EXÉCUTION. |
| 30–43 s | **Le développement** | Restaurant contemporain parisien, rooftop, beach club à Saint-Tropez, brasserie premium, resort international, restaurant gastronomique, réunion de direction, toast de clients au coucher du soleil | DÉVELOPPER LES CONCEPTS. / SUBLIMER L'EXPÉRIENCE. / OPTIMISER LA PERFORMANCE. |
| 43–55 s | **La signature** | Grande salle d'exception (lent mouvement de grue arrière), puis noir et apparition du logo | RESTO CONSEIL · *Des concepts singuliers. Des performances durables.* · CONSEIL • CRÉATION • DÉVELOPPEMENT · www.resto-conseil.com |

Dans chaque plan, une légende discrète précise le métier montré (« Création de concept », « Identité du lieu », « Pilotage de la performance », « Direction opérationnelle »…). Le film parle ainsi de conseil et pas seulement de cuisine.

Toutes les coupes tombent sur les temps de la musique (120 BPM). Chaque début de séquence est marqué par un impact grave (8, 18, 30 et 43 s). La musique ralentit à 43 s : les percussions s'arrêtent et il ne reste que la nappe et le piano. Un impact profond accompagne le logo à 49 s.

## À remplacer avant diffusion

- **Logo** : le monogramme « RC » et le mot-symbole « RESTO CONSEIL » sont **provisoires** (fonction `endCard` dans `index.html`). Envoyez le logo officiel (SVG de préférence) et je l'intègre avec la même animation sobre.
- **URL** : vérifiez que `www.resto-conseil.com` est bien le domaine actif.
- **Photographies de projets** : aucune n'a été fournie, donc tous les décors sont illustrés. Dès que vous les envoyez, chaque plan peut être remplacé par une vraie photo animée en lent travelling, avec la même timeline et les mêmes textes.
- **Musique** : maquette de synthèse calée sur le montage. Pour la diffusion, prévoir une piste sous licence (électro cinématographique, 120 BPM, montée jusqu'à 43 s puis retombée).
- **Contenus fictifs** : la carte (plats d'automne), « Concept — Riviera » et le tableau de bord sans chiffres sont génériques. Le film ne mentionne aucun client, aucune collaboration et aucun indicateur chiffré.

## Version photoréaliste (tournage ou génération vidéo)

Le brief décrit un film en prises de vue réelles 4K, qu'un rendu illustré ne peut pas remplacer. Ce découpage sert de **storyboard et d'animatique** : une production (tournage ou génération vidéo) peut le suivre plan par plan, en gardant les textes, le minutage et la musique.

Consignes communes à tous les plans : *cinematic 4K, photorealistic, anamorphic 35mm look, warm golden-hour grading, cream / deep black / bronze palette, shallow depth of field, slow controlled camera movement, no text, no logos, natural faces or faces out of focus / from behind.*

| # | Temps | Plan |
|---|---|---|
| 1 | 0–3,4 s | Slow dolly forward through an elegant seafront fine-dining room at sunset, floor-to-ceiling windows, white tablecloths, bronze pendant lights, golden light shafts |
| 2 | 3,0–5,8 s | Slow push-in on a Parisian palace hotel façade at blue hour, warm lit windows, glowing entrance canopy |
| 3 | 5,4–8 s | Mediterranean beach restaurant at sunset, straw parasols, string lights, sun glitter on the sea, slow lateral track |
| 4 | 8–10 s | Top-down macro: architect's pen drawing a restaurant floor plan in bronze ink |
| 5 | 10–12 s | Hands laying material samples on a mood board: marble, walnut, brushed brass, linen, terracotta, green velvet |
| 6 | 12–14 s | Menu proof on a walnut table, a pencil circles one dish, warm side light |
| 7 | 14–18 s | Top-down: chef's tweezers placing micro-herbs on a pigeon dish with a beetroot brush stroke, then macro close-up |
| 8 | 18–20 s | Professional kitchen in full service, flames, heat lamps on the pass, order tickets on the rail (focus on the pass) |
| 9 | 20–22 s | Over-the-shoulder of an executive chef overseeing his brigade, chef out of focus |
| 10 | 22–24 s | Palace dining room, crystal chandeliers, waiter crossing with a silver cloche |
| 11 | 24–26 s | Lively destination restaurant, backlit bar, bokeh, guests from behind |
| 12 | 26–28 s | Top-down work table: concept boards, menu drafts, floor plan, swatches |
| 13 | 28–30 s | Tablet showing performance charts (no readable figures), warm reflection sweep |
| 14–19 | 30–39 s | 1,5 s per universe: Paris contemporary bistro, rooftop at night, Saint-Tropez beach club (white parasols, turquoise sea), premium brasserie (globes, mirrors, checkerboard floor), resort infinity pool at sunset, intimate gastronomic room with spotlights |
| 20 | 39–41 s | Management meeting silhouetted against a bright window, floor plan on the board |
| 21 | 41–43,6 s | Close-up of two champagne flutes clinking against the setting sun |
| 22 | 43–49 s | Crane-out revealing a grand restaurant with arched windows and chandeliers, lively and warm |
| 23 | 49–55 s | Black background, logo, signature |
