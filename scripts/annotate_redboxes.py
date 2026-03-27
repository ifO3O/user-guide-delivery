#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _hex_to_rgb(color: str):
    c = (color or "").strip().lstrip("#")
    if len(c) != 6:
        return (231, 76, 60)
    return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))


def _get_font(size: int):
    for f in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _read_spec(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if "images" not in data or not isinstance(data["images"], list):
        raise ValueError("spec must contain an 'images' array")
    return data


def _box_to_xyxy(box: dict):
    if all(k in box for k in ("x", "y", "w", "h")):
        x1 = int(box["x"])
        y1 = int(box["y"])
        x2 = x1 + int(box["w"])
        y2 = y1 + int(box["h"])
        return x1, y1, x2, y2
    if all(k in box for k in ("x1", "y1", "x2", "y2")):
        return int(box["x1"]), int(box["y1"]), int(box["x2"]), int(box["y2"])
    raise ValueError(f"invalid box format: {box}")


def annotate_one(image_path: Path, output_path: Path, boxes: list, style: dict):
    line_color = _hex_to_rgb(style.get("color", "#E74C3C"))
    line_width = int(style.get("line_width", 4))
    badge_size = int(style.get("badge_size", 30))
    badge_radius = int(style.get("badge_radius", 8))
    text_size = int(style.get("text_size", 20))
    text_color = _hex_to_rgb(style.get("text_color", "#FFFFFF"))

    im = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(im)
    font = _get_font(text_size)

    for idx, box in enumerate(boxes, start=1):
        x1, y1, x2, y2 = _box_to_xyxy(box)
        label = str(box.get("label", idx))

        for w in range(line_width):
            draw.rectangle((x1 - w, y1 - w, x2 + w, y2 + w), outline=line_color)

        bx1 = max(6, x1 + 8)
        by1 = max(6, y1 + 8)
        bx2 = bx1 + badge_size
        by2 = by1 + badge_size
        draw.rounded_rectangle(
            (bx1, by1, bx2, by2), radius=badge_radius, fill=line_color
        )

        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = bx1 + (badge_size - tw) / 2
        ty = by1 + (badge_size - th) / 2 - 1
        draw.text((tx, ty), label, fill=text_color, font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Annotate screenshots with red boxes.")
    parser.add_argument("--spec", required=True, help="Path to redbox JSON spec")
    parser.add_argument(
        "--input-dir", required=True, help="Directory containing source screenshots"
    )
    parser.add_argument(
        "--output-dir", required=True, help="Directory for annotated screenshots"
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    data = _read_spec(spec_path)
    style = data.get("style", {})
    images = data["images"]

    for item in images:
        source = item.get("source")
        target = item.get("target")
        boxes = item.get("boxes", [])
        if not source or not target:
            raise ValueError("each image item must contain source and target")
        if not isinstance(boxes, list):
            raise ValueError("boxes must be a list")

        source_path = input_dir / source
        target_path = output_dir / target
        if not source_path.exists():
            raise FileNotFoundError(f"source image not found: {source_path}")
        annotate_one(source_path, target_path, boxes, style)
        print(f"[OK] {target_path}")


if __name__ == "__main__":
    main()
