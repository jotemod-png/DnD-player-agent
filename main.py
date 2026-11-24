import re
from pathlib import Path

from mistralai import agents

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

_DICE_RE = re.compile(r"^\s*(\d*)[dD](\d+)\s*([+-]\s*\d+)?\s*$")


@agents.tool(model_access="direct")
async def rol_dobbelsteen(
    notatie: str,
    label: str = "",
) -> dict[str, object]:
    """Gooi dobbelstenen voor een D&D-worp, bijvoorbeeld 'd20+3', '2d6+2' of 'd20'.

    Args:
        notatie: dobbelnotatie zoals 'd20+3' of '2d6-1' (maximaal 20 dobbelstenen,
                zijden 2, 3, 4, 6, 8, 10, 12, 20 of 100).
        label: waar de worp voor is, bijvoorbeeld 'Perception' of 'schade longsword'.

    Returns:
        dict met de individuele worpen, de modifier en het totaal.
    """
    match = _DICE_RE.match(notatie)
    if not match:
        raise agents.ToolError(
            f"Onbekende dobbelnotatie '{notatie}'. Gebruik bijvoorbeeld 'd20+3' of '2d6-1'."
        )
    aantal = int(match.group(1) or "1")
    zijdig = int(match.group(2))
    modifier = int((match.group(3) or "0").replace(" ", ""))
    if not 1 <= aantal <= 20 or zijdig not in (2, 3, 4, 6, 8, 10, 12, 20, 100):
        raise agents.ToolError(
            f"'{notatie}' valt buiten de toegestane worpen (1-20 dobbelstenen, "
            "zijden 2/3/4/6/8/10/12/20/100)."
        )
    worpen = [agents.random().randint(1, zijdig) for _ in range(aantal)]
    resultaat: dict[str, object] = {
        "notatie": notatie,
        "worpen": worpen,
        "modifier": modifier,
        "totaal": sum(worpen) + modifier,
        "label": label or "worp",
    }
    if aantal == 1 and zijdig == 20:
        resultaat["nat"] = "nat 20" if worpen[0] == 20 else ("nat 1" if worpen[0] == 1 else "")
    return resultaat


agent = agents.Agent(
    model="magistral-medium-latest",
    name="dnd-gm-agent",
    instructions=INSTRUCTIONS,
    tools=[rol_dobbelsteen],
)
