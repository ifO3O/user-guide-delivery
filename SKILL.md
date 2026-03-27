---
name: user-guide-delivery
description: Create external-facing product user manuals with real page screenshots, red-box annotations, and step-by-step guidance. Use when users ask for 对外交付文档, 用户使用手册, 图文教程, 截图标注, 红框说明, or Markdown-to-Word/PDF delivery packs.
---

# User Guide Delivery

## Overview
Generate a delivery-ready user manual for a live web product: real screenshots, red-box callouts, and clean step-by-step instructions.  
Produce three outputs by default: `*.md`, `*.docx`, and `*.pdf`.

## Workflow
1. Collect inputs:
- Audience and style (`外部客户`, `内部培训`, etc.).
- Slogan/brand line to place on top.
- Target pages and desired output language.

2. Capture real screenshots:
- Use Playwright (or equivalent) to log in and open each target page.
- Save raw screenshots into `docs/assets/user-guide/`.
- Prefer fixed viewport for consistency (for example `1600x1100`).

3. Define red-box callouts:
- Create a JSON spec with image-by-image box coordinates.
- Save spec as `docs/assets/user-guide-annotated/redbox-spec.json`.
- Use the script `scripts/annotate_redboxes.py` to generate annotated images.

4. Write the guide markdown:
- Start from `assets/external-user-guide-template.md`.
- Replace placeholders with actual page flow and callout explanations.
- Embed annotated images with relative paths.

5. Export delivery files:
- Use Pandoc to generate DOCX.
- Generate PDF via Pandoc+HTML or browser print.

## Commands
Use the script:

```bash
python scripts/annotate_redboxes.py \
  --spec docs/assets/user-guide-annotated/redbox-spec.json \
  --input-dir docs/assets/user-guide \
  --output-dir docs/assets/user-guide-annotated
```

Use Pandoc:

```bash
pandoc docs/<guide>.md --resource-path=docs -o docs/<guide>.docx
pandoc docs/<guide>.md --resource-path=docs -s -o docs/<guide>.html
```

Then print `docs/<guide>.html` to PDF (A4, print background on).

## Quality Bar
Before final delivery, verify:
- Every screenshot is real, current, and readable.
- Each red box has a matching numbered explanation.
- No internal debug fields are exposed.
- Slogan/brand wording is correct.
- `md/docx/pdf` filenames and dates are consistent.

## References
- Red-box JSON format and coordinate notes: `references/redbox-spec.md`
- Guide template: `assets/external-user-guide-template.md`
