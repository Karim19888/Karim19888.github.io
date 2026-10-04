# الموطور وأول قطرات الشتا — vidéo verticale 9:16

Vidéo de 60 s **avec la voix off de Yassine (ElevenLabs v4)** : 50 s de contenu, 5 s de CTA de partage et 5 s de crédits, 1080×1920, 30 i/s, faite pour Reels, TikTok et Shorts.

## Fichiers

| Fichier | Contenu |
|---|---|
| `moto_premiere_pluie_9x16.mp4` | La vidéo finale : graphismes, voix off, sous-titres darija incrustés et musique |
| `voix_off_yassine_v4.mp3` | La voix off ElevenLabs v4 d'origine (53,9 s) |
| `musique_sans_voix.wav` | La bande-son seule, pour mixer une voix off par-dessus |
| `SOUS_TITRES_DARIJA_V2.srt` | Les sous-titres calés sur la voix, CTA compris |
| `VOIX_OFF_ELEVENLABS_V4.txt` | Le script à coller dans ElevenLabs v4, avec les balises de jeu et le CTA |
| `VOIX_OFF_ELEVENLABS_V4.md` | Les réglages, le calage bloc par bloc et les corrections de prononciation |
| `src/video.html` | Le moteur d'animation (canvas). Ouvrir `src/video.html?play` dans un serveur local pour une lecture en direct, ou `?t=12.5` pour voir une image fixe |
| `src/render.mjs` | Rendu image par image avec Playwright et ffmpeg |
| `src/audio.py` | La bande-son synthétisée (pluie, nappe, pulsation et impacts aux transitions) |
| `src/align.py` | L'alignement du script sur les silences de la voix ; écrit `src/timeline.json` |
| `src/timeline.json` | Le début de chaque scène et les sous-titres, calés sur la voix (décalage de 0,4 s) |

## Ce qui a été changé par rapport au pack

- **Format vertical 9:16** : c'est le format des réseaux où circule le contenu moto au Maroc.
- **Lisible sans le son** : le pack ne contient aucune voix. Chaque phrase du script est donc sous-titrée, avec un titre graphique par séquence.
- **Sous-titres redécoupés** : la version d'origine laissait des mots seuls à l'écran (« والطريق. », « الفكرة. »). Les nouvelles coupures suivent le sens de la phrase.
- **V04 (analogie du zellige)** : le pack réutilisait P02, ce qui faisait 3 apparitions du même pneu. Cette séquence est remplacée par un **zellige animé** (étoiles à 8 branches, film d'eau, bulles de savon, semelle). Le message est le même, l'identité marocaine en plus. La mention « تشبيه توضيحي، ماشي نفس المواد » reste affichée.
- **Identité visuelle marocaine** : transitions en étoile de zellige, palette ambre, rouge et vert, panneau de danger, titres en Lalezar et Cairo.
- **Graphismes explicatifs** : zone de contact du pneu, jauge d'adhérence, schéma d'un virage avec la zone où ralentir, cartes de gestes, cercles autour des marquages et des plaques, manomètre.
- **Aucun chiffre inventé** : la jauge d'adhérence et le manomètre n'ont pas de graduations chiffrées. Le manomètre renvoie à « توصية المصنع » et ajoute « قيس الضغط والرويضات باردين » (pression à froid, source S03).
- **Honnêteté des images** : l'étiquette « صور توضيحية » reste affichée sur chaque photo. La carte finale précise que les photos ne sont pas prises au Maroc ou que le lieu n'est pas confirmé.
- **CTA de partage (59–64 s)** : « صيفط هاد الفيديو لصاحبك مول الموطور… باش يوصل حتى هو سالم ». À l'écran : une bulle de message avec la miniature de la vidéo, un avion en papier qui part et « ولا دير ليه منشن فالتعليقات ». Le fond P05 montre deux motards, ce qui rappelle l'idée de l'ami.
- **Crédits et licences** : auteurs et licences des 6 photos en fin de vidéo, avec la mention « Photos recadrées, étalonnées et annotées » qu'exigent les licences CC BY et CC BY-SA. Les photos P01, P03 et P04 sont en CC BY-SA : la vidéo qui les modifie doit donc être partagée sous **CC BY-SA**.

## Calage sur la voix

La voix (53,9 s) est plus rapide que le découpage du pack (59 s). La vidéo est donc recalée sur elle :

1. `src/align.py` repère les 19 segments de parole (les silences entre les phrases), puis répartit les phrases du script sur ces segments selon leur longueur. Chaque silence tombe sur une fin de phrase.
2. Chaque scène commence pendant la respiration qui précède son texte, et les sous-titres suivent la voix segment par segment.
3. Dans chaque scène, les animations clés sont posées sur les mots : « غبار » et « الزيوت » apparaissent quand ils sont prononcés, « التشبّت كينقص » aussi, les plaques et marquages arrivent sur « ورد بالك », etc. Ce sont les ancres `warp` de `SCENES` dans `src/video.html`.
4. Mixage : la voix est normalisée et légèrement compressée, puis la musique baisse automatiquement quand elle parle (compression sidechain). Volume final : environ −15 LUFS, adapté à Instagram et TikTok.

## Refaire le rendu avec une autre prise de voix

```bash
cd src
# 1. relever les silences de la nouvelle voix, les reporter dans `segs` de align.py, puis :
python3 align.py
# 2. vidéo et musique
PW=$(npm root -g)/playwright node render.mjs video ../silent.mp4 30
python3 audio.py ../musique_sans_voix.wav
# 3. mixage voix + musique avec ducking
ffmpeg -i ../musique_sans_voix.wav -i ../voix_off_yassine_v4.mp3 -filter_complex "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=7,adelay=400|400,apad[v];[v]asplit=2[v1][vsc];[0:a]volume=-3dB[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[md];[md][v1]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[out]" -map "[out]" mix.wav
ffmpeg -i ../silent.mp4 -i mix.wav -c:v libx264 -b:v 3200k -c:a aac -b:a 192k -shortest -movflags +faststart ../moto_premiere_pluie_9x16.mp4
```
