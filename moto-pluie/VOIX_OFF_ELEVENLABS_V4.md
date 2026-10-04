# Voix off : ElevenLabs v4

Le texte prêt à coller est dans **`VOIX_OFF_ELEVENLABS_V4.txt`**. C'est le script court approuvé, sans aucun mot changé, avec les balises d'intention de v4 et le CTA de partage à la fin.

## Réglages

| Réglage | Valeur |
|---|---|
| Modèle | `eleven_v4` (Eleven v4) |
| Langue | Arabe (`ar`) |
| Voix | Une voix **marocaine** de la Voice Library (chercher « Moroccan » ou « Darija »). C'est le choix qui compte le plus : une voix du Moyen-Orient lira la darija avec le mauvais accent. Prendre une voix masculine ou féminine posée, entre 25 et 40 ans, au ton de « grand frère motard » plutôt que publicitaire. |
| Stabilité | Moyenne. Trop basse, la voix en fait trop ; trop haute, elle devient monotone. |
| Durée visée | Environ 63 s : 59 s pour le message et 4 s pour le CTA. |

Les balises entre crochets (`[serious]`, `[calm]`, `[warmly]`, `[short pause]`…) se mettent **en anglais** : v4 les interprète comme des indications de jeu et ne les prononce pas. Chaque balise vaut jusqu'à la suivante. Les points de suspension « … » créent les silences.

## Calage sur la vidéo

La vidéo garde son propre timing. Si la voix est un peu plus rapide ou plus lente, on peut générer **bloc par bloc** (un paragraphe = une séquence) et caler chaque bloc sur son repère :

| Repère | Bloc | Image à l'écran |
|---|---|---|
| 0:00 | غير أول قطرات الشتا… | Panneau de danger + « أول قطرات » |
| 0:06 | الرويضة خاصها تشدّ… | Pneu et zone de contact |
| 0:14 | من بعد مدة بلا شتا… | Poussière, huile, puis la pluie |
| 0:24 | بحال صباطك فوق زليج… | Zellige animé |
| 0:32 | وبالموطور، فالدوران… | Schéma du virage |
| 0:41 | نقص السرعة قبل الدوران… | Cartes de gestes, puis marquages et plaques |
| 0:51 | راقب الرويضات… | Manomètre, puis P06 |
| **0:59** | **صيفط هاد الفيديو لصاحبك مول الموطور…** | **Écran CTA : bulle de message + avion qui part** |
| 1:04 | (silence) | Crédits |

## Si un mot est mal prononcé

v4 accepte la prononciation en API entre barres obliques. Remplacer le mot **seulement s'il sort mal** à la première génération :

| Mot | Remplacement |
|---|---|
| مافزگاتش | `/maːfzɡaːtʃ/` |
| الرويضة | `/rrwiːdˤa/` |
| الرويضات | `/rrwiːdˤaːt/` |
| تفراني | `/tfraːni/` |
| صيفط | `/sˤiːfətˤ/` |

## Mixage

1. Dans CapCut ou Premiere : piste 1 `moto_premiere_pluie_9x16.mp4`, piste 2 la voix.
2. Baisser la musique de 6 à 8 dB pendant que la voix parle, à la main ou avec la fonction de ducking du logiciel.
3. Les sous-titres sont déjà incrustés dans la vidéo. Si la voix décale le timing, `SOUS_TITRES_DARIJA_V2.srt` sert de référence.
