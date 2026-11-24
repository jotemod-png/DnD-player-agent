# D&D 2024 Spelleider-agent

Eén Mistral Agents SDK-agent die het volledige D&D 2024-spelsysteem uit het instructieblok
uitvoert: Agent 1 (Narrator, praat met de DM), Agent 2–5 (Speler A–D), Agent 6 (regel- en
sheetbeheerder) en Agent 7 (logboek en tijdlijn).

## Inhoud

- `main.py` — de agent (`agents.Agent`, model `magistral-medium-latest`) met één vaste tool:
  `rol_dobbelsteen(notatie, label)` voor échte, willekeurige dobbelworpen (d2–d100, max.
  20 dobbelstenen, NAT 20/NAT 1-markering). Geen sandbox, geen code-uitvoering, geen connectors.
- `instructions.md` — het volledige D&D 2024-systeemprompt (secties 0–11) plus de
  toolrichtlijnen (sectie 12).
- `pyproject.toml`, `uv.lock`, `Dockerfile` — scaffold van `agents init`; de deployment
  bouwt de Dockerfile.

## Lokaal draaien

```bash
export MISTRAL_API_KEY="<key met Workflows-rechten>"
uv sync
uv run agents chat          # chat met de locale agent
uv run agents info          # controleer capaciteiten
```

## Deployen (Mistral-managed)

```bash
git add -A && git commit -m "..." && git push -u origin HEAD
uv run --env-file .env agents deploy       # bouwt de gepushte commit
uv run --env-file .env agents chat dnd-gm-agent   # chat met de deployed agent
uv run --env-file .env agents logs dnd-gm-agent --follow
```

Vereisten voor `agents deploy`: de GitHub-connector verbonden in Mistral Studio
(https://console.mistral.ai/build/connectors) en een key van een gebruikersrol met
Workflows-toegang (Developer of Workspace Contributor).

## Spelen

Stuur het eerste bericht met ingevulde sectie 9-sheets (campagne, speelstijl, vier
spelersheets). De agent antwoordt als `[AGENT 1 → DM]`. DM-commando's: `/staat`, `/log`,
`/regel`, `/beknopt`, `/volledig`, `/stap`, `/auto`, `/dobbels dm`, `/dobbels auto`.
Worpen gaan bij DOBBELS: AUTOMATISCH via de vaste tool `rol_dobbelsteen`.
