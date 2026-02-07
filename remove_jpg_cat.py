#!/usr/bin/env python3
"""
remove_jpg_cat.py

Recursively finds and removes files ending with `.jpg.cat` in a directory.

Usage:
  python remove_jpg_cat.py [path] [--dry-run] [--yes]

Defaults to the `cat images` folder in the workspace when no path is provided.
"""
from pathlib import Path
import argparse
import sys


def find_jpg_cat(path: Path):
    if not path.exists():
        print(f"Path not found: {path}")
        return []
    return list(path.rglob("*.jpg.cat"))


def main():
    parser = argparse.ArgumentParser(description="Remove .jpg.cat files")
    parser.add_argument("path", nargs="?", default="cat images",
                        help="Directory to scan (default: 'cat images')")
    parser.add_argument("--dry-run", action="store_true", help="Show files without deleting")
    parser.add_argument("--yes", "-y", action="store_true", help="Actually delete the found files")
    args = parser.parse_args()

    target = Path(args.path)
    files = find_jpg_cat(target)

    if not files:
        print("No .jpg.cat files found.")
        return 0

    print(f"Found {len(files)} .jpg.cat file(s) in '{target}':")
    for f in files:
        print(f" - {f}")

    if args.dry_run:
        print("Dry run: no files will be deleted.")
        return 0

    if not args.yes:
        print("No action taken. Re-run with --yes to delete these files.")
        return 0

    deleted = 0
    errors = 0
    for f in files:
        try:
            f.unlink()
            deleted += 1
        except Exception as e:
            print(f"Failed to delete {f}: {e}")
            errors += 1

    print(f"Deletion complete. Deleted: {deleted}. Errors: {errors}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
