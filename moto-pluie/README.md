# الموطور وأول قطرات الشتا — vidéo verticale 9:16

Vidéo de 64 s (59 s de contenu + 5 s de crédits), 1080×1920, 30 i/s, faite pour Reels, TikTok et Shorts.

## Fichiers

| Fichier | Contenu |
|---|---|
| `moto_premiere_pluie_9x16.mp4` | La vidéo finale : graphismes, sous-titres darija incrustés et musique sans voix |
| `musique_sans_voix.wav` | La bande-son seule, pour mixer une voix off par-dessus |
| `SOUS_TITRES_DARIJA_V2.srt` | Les sous-titres redécoupés et calés sur la vidéo |
| `src/video.html` | Le moteur d'animation (canvas). Ouvrir `src/video.html?play` dans un serveur local pour une lecture en direct, ou `?t=12.5` pour voir une image fixe |
| `src/render.mjs` | Rendu image par image avec Playwright et ffmpeg |
| `src/audio.py` | La bande-son synthétisée (pluie, nappe, pulsation et impacts aux transitions) |

## Ce qui a été changé par rapport au pack

- **Format vertical 9:16** : c'est le format des réseaux où circule le contenu moto au Maroc.
- **Lisible sans le son** : le pack ne contient aucune voix. Chaque phrase du script est donc sous-titrée, avec un titre graphique par séquence.
- **Sous-titres redécoupés** : la version d'origine laissait des mots seuls à l'écran (« والطريق. », « الفكرة. »). Les nouvelles coupures suivent le sens de la phrase.
- **V04 (analogie du zellige)** : le pack réutilisait P02, ce qui faisait 3 apparitions du même pneu. Cette séquence est remplacée par un **zellige animé** (étoiles à 8 branches, film d'eau, bulles de savon, semelle). Le message est le même, l'identité marocaine en plus. La mention « تشبيه توضيحي، ماشي نفس المواد » reste affichée.
- **Identité visuelle marocaine** : transitions en étoile de zellige, palette ambre, rouge et vert, panneau de danger, titres en Lalezar et Cairo.
- **Graphismes explicatifs** : zone de contact du pneu, jauge d'adhérence, schéma d'un virage avec la zone où ralentir, cartes de gestes, cercles autour des marquages et des plaques, manomètre.
- **Aucun chiffre inventé** : la jauge d'adhérence et le manomètre n'ont pas de graduations chiffrées. Le manomètre renvoie à « توصية المصنع » et ajoute « قيس الضغط والرويضات باردين » (pression à froid, source S03).
- **Honnêteté des images** : l'étiquette « صور توضيحية » reste affichée sur chaque photo. La carte finale précise que les photos ne sont pas prises au Maroc ou que le lieu n'est pas confirmé.
- **Crédits et licences** : auteurs et licences des 6 photos en fin de vidéo, avec la mention « Photos recadrées, étalonnées et annotées » qu'exigent les licences CC BY et CC BY-SA. Les photos P01, P03 et P04 sont en CC BY-SA : la vidéo qui les modifie doit donc être partagée sous **CC BY-SA**.

## Ajouter la voix

1. Enregistrer `montage/SCRIPT_DARIJA_60S.txt`, qui dure environ 59 s.
2. Dans CapCut ou Premiere : placer la vidéo, ajouter la voix et baisser la musique d'environ 6 dB sous la voix (ducking).
3. Si la lecture est plus lente ou plus rapide, modifier les temps de `SUBS` dans `src/video.html` puis relancer le rendu :

```bash
cd src
PW=$(npm root -g)/playwright node render.mjs video ../silent.mp4 30
python3 audio.py ../musique_sans_voix.wav
ffmpeg -i ../silent.mp4 -i ../musique_sans_voix.wav -c:v copy -c:a aac -b:a 192k -shortest ../moto_premiere_pluie_9x16.mp4
```
