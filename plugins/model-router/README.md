# model-router

Un seul skill (`skills/model-router/SKILL.md`) : Claude classe chaque tâche (rapide / standard / complexe) et la délègue à un sous-agent Haiku, Sonnet ou Opus via le paramètre `model` de l'outil Agent.

Pas de hook, pas de script. Le déclenchement repose sur la description du skill (non garanti à 100 %) ; `/model-router` force l'application. Lancer la session sur Sonnet (`/model sonnet`).

Installation permanente, dans `~/.claude/settings.json` :

```json
{
  "model": "sonnet",
  "extraKnownMarketplaces": {
    "perso": { "source": { "source": "github", "repo": "pmvkfgz969-web/claude-plugins-official" } }
  },
  "enabledPlugins": { "model-router@perso": true }
}
```
