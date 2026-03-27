# user-guide-delivery

一个用于“对外交付用户手册（含截图与高亮标注）”的 Codex Skill。

## 功能介绍
- 采集真实页面截图
- 根据 JSON 标注规范生成说明高亮提示框说明图
- 生成可交付的图文版 Markdown 手册
- 支持导出为 Word/PDF

## 目录结构
- `SKILL.md`
- `agents/openai.yaml`
- `assets/external-user-guide-template.md`
- `references/redbox-spec.md`
- `scripts/annotate_redboxes.py`

## 快速开始
```bash
python scripts/annotate_redboxes.py \
  --spec docs/assets/user-guide-annotated/redbox-spec.json \
  --input-dir docs/assets/user-guide \
  --output-dir docs/assets/user-guide-annotated
