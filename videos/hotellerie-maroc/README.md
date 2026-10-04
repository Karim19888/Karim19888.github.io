# مرحبا بيك… حتى بالدرهم — vidéo motion design (hôtellerie Maroc)

- **Rendu final** : `marhba-bik-hta-bdirham.mp4` — 1080×1920 (9:16), 30 fps, 86 s, H.264 + AAC.
- **Aperçu web** : `index.html` (lecteur) · `composition.html?play` (animation en direct) · `composition.html?t=42` (image figée).

## Structure (script darija du pack, sans changement de texte)

| Temps | Séquence | Visuel |
|---|---|---|
| 0–9 s | Hook « نفس الفندق… ثمن مختلف » | P04 dans une arche, **floutée + étiquette « صورة توضيحية »**, étiquettes € / درهم sans montant |
| 9–19 s | Remise ≠ traitement | Deux cartes (التخفيض / المعاملة) + signe ≠, source Hespress 18/08/2025 |
| 19–32 s | Plaintes publiées — 2025 | Coupures T02 + T01 recréées (texte exact), surlignage, tampon « 2025 » |
| 32–43 s | Exigence éditoriale | Exemples barrés → « الثمن واضح ✓ / الخدمة محترمة ✓ » |
| 43–55 s | Budget famille | P02 (archive 2015) + équation hôtel + route + repas + enfants |
| 55–68 s | Données ONMT | Compteur +12.1 « مليون ليلة مبيت », anneau 28 %, logo ONMT comme source |
| 68–80 s | Conclusion | P03 + P01 en arches, 3 piliers, slogan calligraphié |
| 80–86 s | Crédits | Sources + licences CC BY-SA |

## Choix ajoutés par rapport au pack

1. **Direction artistique** (absente du pack) : arches mauresques comme cadres photo, étoile à 8 branches / zellige, palette indigo nuit · terracotta · safran · vert · bleu Majorelle, typos Reem Kufi / Cairo / Aref Ruqaa.
2. **Sous-titres animés de toute la narration** : le pack ne fournit pas de voix off, donc la vidéo se lit seule (muet en scroll). Le SRT reste valable si une voix est enregistrée ensuite.
3. **P04 anonymisée** dans le hook : le pack la place au hook alors que CREDITS.md demande de ne montrer les hôtels identifiables qu'en contexte positif. Floutage + mention « صورة توضيحية · أرشيف 2023 ».
4. **P07 et P08 non utilisées** : « droits réservés, aucune licence acquise ».
5. **Cartes T01–T04 redessinées** (texte exact conservé + mention « ماشي لقطة شاشة ») au lieu des PNG blancs.
6. **Carton crédits** ajouté (+6 s) : la licence CC BY-SA exige auteur, licence et mention des modifications.
7. **Musique originale procédurale** (`music.py`, mode Hijaz, bendir, oud synthétique) : pas de droits tiers.
8. Libellé « ليالي المبيت » partout, jamais « عدد السياح » ; dates d'archive affichées sur chaque photo.

## Régénérer

```bash
ln -s "$(npm root -g)" node_modules          # playwright
node render.mjs frames /tmp/frames 30 6       # images
python3 music.py /tmp/music.wav               # musique (numpy)
ffmpeg -framerate 30 -i /tmp/frames/f%05d.jpg -i /tmp/music.wav \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k \
  -shortest -movflags +faststart marhba-bik-hta-bdirham.mp4
```
