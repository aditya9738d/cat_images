# cat_images

This repository contains resized cat images generated from a local dataset. Use the scripts in the repository to re-run the resizing or adjust parameters.

Files added by the helper scripts:
- `remove_jpg_cat.py` — cleanup script that removed `.jpg.cat` files
- `resize_images.py` — resizes JPEGs and writes to `cat images_resized`

Usage examples:

```bash
python resize_images.py "cat images" --output "cat images_resized" --max-dim 1024 --quality 85
```
