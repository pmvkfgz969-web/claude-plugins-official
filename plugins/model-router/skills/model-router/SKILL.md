---
name: model-router
description: Économie de tokens. À appliquer au début de chaque tâche non triviale pour choisir le modèle le moins cher suffisant (Haiku, Sonnet ou Opus) et lui déléguer le travail via l'outil Agent. Invocable aussi avec /model-router.
---

# Routage par modèle

Avant d'agir, classe la demande, puis délègue avec l'outil Agent en passant le paramètre `model`. Brief autonome et concis ; relaie la conclusion sans la réécrire.

| Niveau | `model` | Cas |
|---|---|---|
| Rapide | `haiku` | recherche de fichier/symbole, lecture, résumé, reformatage, renommage, git/shell trivial, traduction |
| Standard | `sonnet` | implémenter, corriger un bug localisé, écrire des tests, modifier quelques fichiers, rédiger |
| Complexe | `opus` | architecture, refactor transverse, bug difficile ou intermittent, sécurité, performance, décision à fort enjeu |

Règles :
- Dans le doute entre deux niveaux, prends le plus bas ; escalade d'un niveau si le sous-agent signale que c'est plus dur que prévu.
- Ne délègue pas si la réponse tient en une phrase sans outil, ou si tu es déjà au niveau requis ou en dessous.
- Un préfixe `!haiku`, `!sonnet`, `!opus` dans le prompt impose le niveau ; `!raw` désactive le routage pour ce prompt.
- Pour que le gain soit réel, la session principale doit tourner sur Sonnet (`/model sonnet`).
