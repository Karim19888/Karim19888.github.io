# ورا الطلبية… شنو كيبقى — vidéo 59 s (9:16)

- `LIVRAISON_59S_1080x1920.mp4` : version finale (motion design + musique, sous-titres darija incrustés).
- `LIVRAISON_59S_sans_musique.mp4` : même image, sans audio (pour poser la voix off).
- `source/` : animation HTML/JS rendue image par image avec Playwright, puis encodée avec ffmpeg.

## Recréer la vidéo

```bash
cd source
npm i playwright
node render.js preview 3,15,45        # aperçus JPG
node render.js video silent.mp4 30    # rendu complet
python3 music.py                      # musique -> music.wav (numpy)
ffmpeg -i silent.mp4 -i music.wav -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

## Garde-fous éditoriaux repris du pack

- Tous les chiffres sont une **simulation** (bandeau «مثال افتراضي» de 6 à 47 s ; «ماشي ربح صافي» sur le 28).
- La plateforme du calcul est générique : le logo Glovo apparaît uniquement sur la carte des sources finale.
- Chaque photo porte son crédit et son lieu (Madrid légendée «إسبانيا · أرشيف»).
- ⚠️ La photo P01 (Mustapha Razi / Le Desk) est en **droits réservés, aucune licence acquise**, et porte le filigrane Le Desk : obtenir l'autorisation avant de publier, sinon la remplacer par une photo à toi ou par P02.
