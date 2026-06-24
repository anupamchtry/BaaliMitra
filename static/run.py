from __future__ import annotations

import argparse
import random
from pathlib import Path

from PIL import Image


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def list_images(folder: Path) -> list[Path]:
    return sorted(
        [
            p for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS
        ],
        key=lambda p: p.name.lower()
    )


def to_safe_label(relative_folder: Path) -> str:
    # Turn nested paths into a single safe label (e.g., "A/B" -> "A_B")
    return str(relative_folder).replace("\\", "_").replace("/", "_")


def save_as_jpg(src: Path, dst: Path, quality: int = 95) -> None:
    with Image.open(src) as im:
        # Ensure RGB for JPEG
        if im.mode != "RGB":
            im = im.convert("RGB")
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, format="JPEG", quality=quality, optimize=True)


def iter_target_folders(root: Path, recursive: bool) -> list[Path]:
    if not recursive:
        return sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.name.lower())

    # Recursive: take all subdirectories (excluding root itself) that contain images
    folders = []
    for d in root.rglob("*"):
        if d.is_dir():
            if any((f.is_file() and f.suffix.lower() in IMAGE_EXTS) for f in d.iterdir()):
                folders.append(d)
    return sorted(folders, key=lambda p: str(p).lower())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Grab N images from each folder and copy as JPG into a destination folder."
    )
    parser.add_argument("source_root", type=str, help="Root folder containing subfolders of images")
    parser.add_argument("dest_folder", type=str, help="Destination folder to collect images into")
    parser.add_argument("--per-folder", type=int, default=3, help="How many images to pick per folder (default: 3)")
    parser.add_argument("--random", action="store_true", help="Pick random images instead of first N sorted")
    parser.add_argument("--recursive", action="store_true", help="Also process nested subfolders recursively")
    args = parser.parse_args()

    root = Path(args.source_root).expanduser().resolve()
    dest = Path(args.dest_folder).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Source root does not exist or is not a folder: {root}")

    folders = iter_target_folders(root, recursive=args.recursive)
    if not folders:
        print("No subfolders with images found.")
        return 0

    for folder in folders:
        images = list_images(folder)
        if not images:
            continue

        k = min(args.per_folder, len(images))
        chosen = random.sample(images, k) if args.random else images[:k]

        label = to_safe_label(folder.relative_to(root))

        for i, img_path in enumerate(chosen, start=1):
            out_path = dest / f"{label}_{i}.jpg"
            save_as_jpg(img_path, out_path)

        print(f"Processed: {folder}  -> saved {len(chosen)} file(s) as {label}_#.jpg")

    print(f"\nDone. Output folder: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
