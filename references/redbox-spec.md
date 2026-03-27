# Red-Box Spec

## JSON schema

```json
{
  "style": {
    "color": "#E74C3C",
    "line_width": 4,
    "badge_size": 30,
    "badge_radius": 8,
    "text_size": 20,
    "text_color": "#FFFFFF"
  },
  "images": [
    {
      "source": "01-home.png",
      "target": "01-home-annotated.png",
      "boxes": [
        { "label": "1", "x": 280, "y": 130, "w": 340, "h": 250 },
        { "label": "2", "x": 640, "y": 130, "w": 340, "h": 250 }
      ]
    }
  ]
}
```

## Coordinate rules

- `x`, `y` are top-left origin in pixels.
- `w`, `h` are width and height in pixels.
- You can also use `{x1,y1,x2,y2}`.
- Keep a consistent browser viewport across pages for easier annotation.

## Suggested capture settings

- Desktop guide: `1600x1100`
- Full-page when content is long, viewport screenshot when only hero area is needed.

