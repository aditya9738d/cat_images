#!/usr/bin/env python3
"""
resize_images.py

Resize and recompress JPEG images to reduce file size while preserving quality.

Usage:
  python resize_images.py [input_dir] [--output OUT] [--max-dim N] [--quality Q] [--workers N] [--dry-run] [--inplace]

Default: scans `cat images`, writes resized copies to `cat images_resized`.
"""
from pathlib import Path
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image


def process_image(src: Path, dst: Path, max_dim: int, quality: int, dry_run: bool):
    try:
        if dry_run:
            return (src, None)
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as im:
            im = im.convert("RGB")
            # Resize preserving aspect ratio
            im.thumbnail((max_dim, max_dim), Image.LANCZOS)
            im.save(dst, format="JPEG", quality=quality, optimize=True, progressive=True)
        return (src, dst)
    except Exception as e:
        return (src, e)


def gather_images(path: Path):
    exts = (".jpg", ".jpeg", ".JPG", ".JPEG")
    return [p for p in path.rglob("*") if p.suffix in exts and p.is_file()]


def main():
    parser = argparse.ArgumentParser(description="Resize and recompress JPEG images")
    parser.add_argument("input", nargs="?", default="cat images",
                        help="Input directory (default: 'cat images')")
    parser.add_argument("--output", "-o", default="cat images_resized",
                        help="Output directory (default: 'cat images_resized')")
    parser.add_argument("--max-dim", type=int, default=1024,
                        help="Maximum width/height in pixels (default: 1024)")
    parser.add_argument("--quality", type=int, default=85,
                        help="JPEG quality 1-100 (default: 85)")
    parser.add_argument("--workers", type=int, default=8,
                        help="Number of worker threads (default: 8)")
    parser.add_argument("--dry-run", action="store_true", help="Show files that would be processed")
    parser.add_argument("--inplace", action="store_true", help="Overwrite originals instead of writing to output dir")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"Input directory not found: {input_dir}")
        return 1

    images = gather_images(input_dir)
    if not images:
        print("No JPEG images found.")
        return 0

    print(f"Found {len(images)} JPEG image(s) under '{input_dir}'")

    out_dir = Path(args.output) if not args.inplace else input_dir

    tasks = []
    with ThreadPoolExecutor(max_workers=args.workers) as exe:
        futures = {}
        for src in images:
            # Preserve relative structure
            rel = src.relative_to(input_dir)
            dst = out_dir / rel
            if args.inplace:
                dst = src
            futures[exe.submit(process_image, src, dst, args.max_dim, args.quality, args.dry_run)] = src

        processed = 0
        errors = 0
        for fut in as_completed(futures):
            src, result = fut.result()
            if args.dry_run:
                print(f"Would process: {src}")
            else:
                if isinstance(result, Path):
                    processed += 1
                else:
                    errors += 1
                    print(f"Error processing {src}: {result}")

    if args.dry_run:
        print("Dry run complete. No files were changed.")
    else:
        print(f"Resizing complete. Processed: {processed}. Errors: {errors}.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
