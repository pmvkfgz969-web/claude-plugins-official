#!/usr/bin/env python3
"""UserPromptSubmit hook : classification heuristique (zéro token) du prompt.

Injecte une consigne courte demandant de déléguer à router-quick (Haiku),
router-standard (Sonnet) ou router-deep (Opus). Préfixes manuels : !quick, !std, !deep, !raw
(!raw = aucun routage pour ce prompt).
"""
import json
import os
import re
import sys

STATE = os.path.join(
    os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.expanduser("~/.claude/model-router"),
    "mode",
)

DEEP = re.compile(
    r"architect|refactor|refonte|root cause|cause racine|race condition|deadlock|fuite m[ée]moire|memory leak|"
    r"s[ée]curit|vuln[ée]rab|audit|migration|performance|optimis|concurren|trade-?off|strat[ée]gi|"
    r"con[çc]ois|design|d[ée]bug.*(complexe|difficile|intermittent|al[ée]atoire)|intermittent|non reproductible|"
    r"pourquoi.*(plante|[ée]choue|crash)|analyse approfondie|compar(e|er).*(option|approche|solution)",
    re.I,
)
QUICK = re.compile(
    r"^(liste|list|cherche|trouve|find|grep|où (est|se trouve)|montre|affiche|show|lis |read |"
    r"renomme|rename|formate|format|traduis|translate|r[ée]sume|summari[sz]e|git (status|log|diff)|"
    r"combien|quel(le)? est le (nom|chemin)|ouvre|ajoute (un|une) (commentaire|import)|corrige (la|une) (faute|typo))",
    re.I,
)

TIERS = {
    "quick": ("router-quick", "Haiku"),
    "std": ("router-standard", "Sonnet"),
    "deep": ("router-deep", "Opus"),
}


def classify(prompt: str) -> str:
    p = prompt.strip()
    if DEEP.search(p) or len(p) > 1500:
        return "deep"
    if len(p) < 220 and QUICK.search(p):
        return "quick"
    if len(p) < 60 and "\n" not in p and not re.search(r"\b(impl|cr[ée]e|[ée]cris|ajoute|corrige|fix|build|write)", p, re.I):
        return "quick"
    return "std"


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    try:
        mode = open(STATE).read().strip()
    except OSError:
        mode = "on"
    if mode == "off":
        return

    prompt = data.get("prompt", "")
    if prompt.lstrip().startswith("/"):
        return  # commandes slash : ne pas interférer

    m = re.match(r"\s*!(quick|std|deep|raw)\b", prompt)
    tier = m.group(1) if m else classify(prompt)
    if tier == "raw":
        return

    agent, model = TIERS[tier]
    msg = (
        f"[model-router] Niveau détecté : {tier} → sous-agent `{agent}` ({model}). "
        f"Délègue l'exécution via l'outil Agent (subagent_type=\"{agent}\") avec un brief autonome et concis, "
        "puis relaie sa conclusion sans la réécrire. "
        "Exceptions : fais-le toi-même si tu es déjà au niveau ou en dessous, "
        "ou si la réponse tient en une phrase sans outil. "
        "Si le sous-agent signale une tâche plus dure que prévu, escalade d'un niveau."
    )
    print(json.dumps({
        "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}
    }))


main()
