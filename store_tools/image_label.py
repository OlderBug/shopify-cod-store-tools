"""Add a small, bold colour label to a product image.

Style: ``COLOR: POLO BLUE``, bottom corner, never the centre,
no background bar, no extra canvas. The image keeps its exact size.
Only a thin dark outline around the letters keeps it readable.
"""

from PIL import Image, ImageDraw, ImageFont


def load_bold_font(image_width: int, scale: float):
    size = max(16, int(image_width * scale))
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def label_image(input_path, output_path, color,
                corner="bottom-left", scale=0.035):
    image = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    text = f"COLOR: {color.strip().upper()}"
    font = load_bold_font(image.width, scale)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=2)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    margin = max(12, int(image.width * 0.015))
    y = image.height - text_h - margin
    x = image.width - text_w - margin if corner == "bottom-right" else margin
    draw.text((x, y), text, font=font, fill="white",
              stroke_width=2, stroke_fill="black")
    image.save(output_path)
    return output_path
