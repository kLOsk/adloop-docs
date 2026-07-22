"""Generate reference/tools.mdx from the live AdLoop tool registry.

The tool reference is NEVER hand-edited — it is derived from the same
registry the MCP server serves, so it cannot drift from reality.

Run from the docs repo root:

    uv run --project ../adloop python scripts/generate_tools.py
"""

import asyncio
import pathlib

from adloop.server import TOOLSETS, mcp

LABELS = {
    "core": "Always available",
    "ads": "Google Ads",
    "ga4": "Google Analytics",
    "tracking": "Tracking & Attribution",
    "gtm": "Tag Manager",
    "gsc": "Search Console",
    "web": "Web Performance",
    "merchant": "Merchant Center",
}

HEADER = """---
title: "Tool reference"
description: "Every AdLoop tool, grouped by toolset."
---

{/* GENERATED FILE — do not edit by hand.
    Regenerate: uv run --project ../adloop python scripts/generate_tools.py */}

Tools are grouped by [toolset](/concepts/toolsets). Type: **Read** tools never change anything; **Write** tools return previews and only act through `confirm_and_apply`; **Destructive** writes additionally require double confirmation.
"""


def tool_type(tool) -> str:
    ann = getattr(tool, "annotations", None)
    if ann is not None and getattr(ann, "destructiveHint", False):
        return "Destructive"
    if ann is not None and getattr(ann, "readOnlyHint", False):
        return "Read"
    return "Write"


def summary(tool) -> str:
    line = (tool.description or "").strip().split("\n")[0].strip()
    return (
        line.replace("|", "\\|")
        .replace("{", "&#123;")
        .replace("}", "&#125;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main() -> None:
    tools = asyncio.run(mcp.list_tools())
    known = set(TOOLSETS) | {"core"}
    by_set: dict[str, list] = {slug: [] for slug in ["core", *TOOLSETS]}
    for tool in sorted(tools, key=lambda t: t.name):
        tag = next(iter((tool.tags or set()) & known))
        by_set[tag].append(tool)

    parts = [HEADER]
    for slug, bucket in by_set.items():
        if not bucket:
            continue
        parts.append(f"\n## {LABELS[slug]} (`{slug}`)\n")
        if slug == "core":
            parts.append("Included with every toolset selection.\n")
        else:
            parts.append(f"{TOOLSETS[slug]}.\n")
        parts.append("| Tool | Type | What it does |")
        parts.append("|------|------|--------------|")
        for tool in bucket:
            parts.append(f"| `{tool.name}` | {tool_type(tool)} | {summary(tool)} |")
        parts.append("")

    out = pathlib.Path(__file__).resolve().parent.parent / "reference" / "tools.mdx"
    out.write_text("\n".join(parts))
    print(f"wrote {out} ({sum(len(b) for b in by_set.values())} tools)")


if __name__ == "__main__":
    main()
