# model-router

Mode d'économie de tokens. Chaque prompt est classé par une heuristique locale (aucun appel modèle), puis Claude reçoit la consigne de déléguer à un sous-agent au bon modèle :

| Niveau | Sous-agent | Modèle | Cas typiques |
|---|---|---|---|
| quick | `router-quick` | Haiku | recherche, lecture, résumé, renommage, git trivial |
| std | `router-standard` | Sonnet | implémentation, bug localisé, tests, rédaction |
| deep | `router-deep` | Opus | architecture, refactor transverse, debug dur, sécurité, perf |

## Utilisation

- `/router on|off|status` — active/désactive (actif par défaut).
- Forcer un niveau sur un prompt : préfixe `!quick`, `!std`, `!deep`, ou `!raw` (aucun routage).

## Limites

- Un hook ne peut pas changer le modèle de la session principale : celle-ci lit la consigne et délègue. Lance ta session sur **Sonnet** (`/model sonnet`) ; Opus en session principale annule l'essentiel du gain.
- Le routage est heuristique (mots-clés + longueur). Ajuste les regex dans `hooks/route.py` à ton usage.
- Déléguer coûte un aller-retour : sur une question d'une phrase, Claude répond directement.
