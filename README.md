# adloop-docs

Documentation for AdLoop and AdLoop Cloud, published with
[Mintlify](https://mintlify.com) at docs.getadloop.com (once connected).

One site for both editions on purpose: the products share their tools and
safety model, so the docs share everything except the setup paths. The
quickstart is the fork in the road; "AdLoop Cloud" and "Self-hosting"
groups hold the product-specific pages.

## Working on the docs

```bash
npm i -g mint     # once
mint dev          # local preview at localhost:3000
```

Pages are MDX; navigation lives in `docs.json`. English only for now
(decision 2026-07-22: DE only if support traffic demands it).

## Generated content — do not hand-edit

`reference/tools.mdx` is generated from the live OSS tool registry so it
can never drift from what the server actually ships:

```bash
uv run --project ../adloop python scripts/generate_tools.py
```

Regenerate after any tool or toolset change in the `adloop` repository
(sibling checkout expected at `../adloop`).

## Style

Follow the brand voice (see `../brandkit/BRAND.md`): direct,
practitioner-to-practitioner, concrete claims, numbers only when measured.
Never state tool counts in prose — they rot; the generated reference is
the only place counts may appear, because it regenerates.

## Publishing

Mintlify deploys on push once the GitHub repo is connected in the
Mintlify dashboard. The published site auto-hosts a read MCP server at
`/mcp` (search + docs tools) — mention it in the docs themselves once live.
