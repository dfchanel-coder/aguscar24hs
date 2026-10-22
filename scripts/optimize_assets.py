#!/usr/bin/env python3
"""Optimiza recursos. Requiere Pillow solo para regenerar las imágenes."""
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "img"
PHOTO_NAMES = [
    "aguscar-camion-rojo1", "aguscar-camion-1", "aguscar-camion-2",
]


def main():
    manifest = {}
    for name in PHOTO_NAMES:
        with Image.open(IMAGES / f"{name}.jpg") as source:
            photo = ImageOps.exif_transpose(source).convert("RGB")
            variants = []
            for width in (480, 960, 1600):
                if width > photo.width:
                    continue
                resized = photo.resize(
                    (width, round(photo.height * width / photo.width)),
                    Image.Resampling.LANCZOS,
                )
                filename = f"{name}-{width}.webp"
                resized.save(IMAGES / filename, "WEBP", quality=78, method=6)
                variants.append({"file": filename, "width": resized.width})
            manifest[name] = {
                "file": f"{name}.jpg", "width": photo.width,
                "height": photo.height, "variants": variants,
            }
    with Image.open(IMAGES / "logo-aguscar.png") as source:
        logo = ImageOps.exif_transpose(source).convert("RGB")
        for size, filename in (
            (256, "logo-aguscar.webp"), (180, "apple-touch-icon.png"),
            (48, "favicon-48.png"), (32, "favicon-32.png"),
        ):
            icon = ImageOps.contain(logo, (size, size), Image.Resampling.LANCZOS)
            if filename.endswith(".webp"):
                icon.save(IMAGES / filename, "WEBP", quality=86, method=6)
            else:
                icon.save(IMAGES / filename, "PNG", optimize=True)
        ImageOps.contain(logo, (256, 256), Image.Resampling.LANCZOS).save(
            IMAGES / "logo-aguscar.png", "PNG", optimize=True
        )
    (ROOT / "content" / "assets.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Recursos optimizados: {len(PHOTO_NAMES)} imágenes y logo.")


if __name__ == "__main__":
    main()
