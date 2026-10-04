# مرحبا بيك… حتى بالدرهم — vidéo motion design (hôtellerie Maroc)

- **Reel (version principale)** : `marhba-bik-reel.mp4` — 1080×1920, 30 fps, **42 s**, H.264 + AAC.
- **Version longue (v1, 86 s)** : `marhba-bik-version-longue.mp4` (archive, la composition actuelle produit le Reel).
- **Aperçu web** : `index.html` · `composition.html?play` · `composition.html?t=2.5`.

## Structure du Reel

| Temps | Beat | Visuel |
|---|---|---|
| 0–1,8 s | **Hook coup de poing** | « نفس الفندق / نفس البيت / نفس الليلة » plein écran, flash + zoom à chaque mot |
| 1,8–4,6 s | Le face-à-face | Écran partagé « هو · جاي من أوروبا ?? € » / « نتا · ساكن فالمغرب ?? درهم », tampon « ثمن مختلف؟ » |
| 4,6–11 s | Remise ≠ traitement | Cartes التخفيض / المعاملة + « ≠ » qui claque |
| 11–16 s | Plaintes publiées 2025 | Coupures T02 + T01, surlignage, tampon 2025 |
| 16–20,5 s | Exigence | Exemples barrés → ✓ الثمن واضح / ✓ الخدمة محترمة |
| 20,5–25,5 s | Budget famille | P02 + équation hôtel + route + repas + enfants |
| 25,5–31,5 s | Données ONMT | +12.1 مليون ليلة مبيت, anneau 28 % |
| 31,5–38 s | Conclusion | P03 + P01, 3 piliers, slogan |
| 38–42 s | Crédits | Sources + licences CC BY-SA |

Sous-titres condensés à partir du script darija (nuances conservées : « يقدر », « عند بعض الفنادق », « عند البعض », « ليالي المبيت »). Aucun montant affiché : « ?? » remplace les prix.

## Choix ajoutés par rapport au pack

1. **Direction artistique** (absente du pack) : arches mauresques comme cadres photo, étoile à 8 branches / zellige, palette indigo nuit · terracotta · safran · vert · bleu Majorelle, typos Reem Kufi / Cairo / Aref Ruqaa.
2. **Sous-titres animés de toute la narration** : le pack ne fournit pas de voix off, donc la vidéo se lit seule (muet en scroll). Le SRT reste valable si une voix est enregistrée ensuite.
3. **P04 anonymisée** dans le hook : le pack la place au hook alors que CREDITS.md demande de ne montrer les hôtels identifiables qu'en contexte positif. Floutage + mention « صورة توضيحية · أرشيف 2023 ».
4. **P07 et P08 non utilisées** : « droits réservés, aucune licence acquise ».
5. **Cartes T01–T04 redessinées** (texte exact conservé + mention « ماشي لقطة شاشة ») au lieu des PNG blancs.
6. **Carton crédits** ajouté (4 s) : la licence CC BY-SA exige auteur, licence et mention des modifications.
7. **Musique originale procédurale** (`music.py`, mode Hijaz, bendir, oud synthétique) : pas de droits tiers.
8. Libellé « ليالي المبيت » partout, jamais « عدد السياح » ; dates d'archive affichées sur chaque photo.

## Régénérer

```bash
ln -s "$(npm root -g)" node_modules          # playwright
node render.mjs frames /tmp/frames 30 6       # 1260 images
python3 music.py /tmp/music.wav               # musique (numpy)
ffmpeg -framerate 30 -i /tmp/frames/f%05d.jpg -i /tmp/music.wav \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k \
  -shortest -movflags +faststart marhba-bik-reel.mp4
```
