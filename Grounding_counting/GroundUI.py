#!/usr/bin/env python3
import os
import json
import shutil
from datasets import load_dataset

def export_groundui(dest_root: str):
    # 1) Load only the "train" split
    cache_dir = "/mnt/VLAI_data/cached_groundui"
    ds = load_dataset(
        "agent-studio/GroundUI-18K",
        split="train",
        cache_dir=cache_dir
    )

    # 2) Prepare output dirs
    images_dir = os.path.join(dest_root, "images")
    os.makedirs(images_dir, exist_ok=True)

    annotations = []

    # 3) Loop through each example
    for sample in ds:
        # derive filename from image_path
        img_path_field = sample["image_path"]
        img_fname = os.path.basename(img_path_field)

        # save PIL image to disk
        img = sample["image"]  # this is a PIL.Image
        out_img = os.path.join(images_dir, img_fname)
        img.save(out_img)

        # collect annotation (omit the actual image object)
        annotations.append({
            "id":          sample["id"],
            "image_path":  img_fname,
            "instruction": sample["instruction"],
            "bbox":        sample["bbox"],
            "resolution":  sample["resolution"],
            "source":      sample["source"],
            "platform":    sample["platform"],
        })

    # 4) Write annotation.json
    ann_path = os.path.join(dest_root, "annotation.json")
    with open(ann_path, "w", encoding="utf-8") as f:
        json.dump(annotations, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(annotations)} records → {ann_path}")

    # 5) Clean up cache
    shutil.rmtree(cache_dir)
    print(f"Removed cache at {cache_dir}")

if __name__ == "__main__":
    DEST = "/mnt/VLAI_data/GroundUI"
    os.makedirs(DEST, exist_ok=True)
    export_groundui(DEST)
