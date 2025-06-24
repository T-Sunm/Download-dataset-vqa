#!/usr/bin/env python3
import os
import json
import shutil
import requests
import zipfile
from tqdm import tqdm
from datasets import load_dataset

def download_and_extract_images_zip(zip_url: str, target_dir: str):
    """
    Download a ZIP archive from `zip_url` and extract its contents under `target_dir`.
    """
    os.makedirs(target_dir, exist_ok=True)
    zip_path = os.path.join(target_dir, "images.zip")
    # Download with progress bar
    resp = requests.get(zip_url, stream=True)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    with open(zip_path, "wb") as f, tqdm(
        desc="Downloading Images ZIP",
        total=total, unit="B", unit_scale=True
    ) as pbar:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    # Extract
    print("Extracting images...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target_dir)

    os.remove(zip_path)
    print(f"  ✓ Images extracted to {target_dir}")

def export_unichart(dest_dir: str):
    # 1) Annotation cache
    ann_cache = "/home/minhtq/workspace/Download-dataset-vqa/cache_annotation"
    ds_ann = load_dataset(
        "ahmed-masry/unichart-pretrain-data",
        cache_dir=ann_cache,
    )

    # 2) Download & extract toàn bộ ảnh vào dest_dir/images/
    images_zip_url = (
        "https://huggingface.co/datasets/ahmed-masry/UniChart-pretrain-images"
        "/resolve/main/UniChart%20Images.zip"
    )
    images_root = os.path.join(dest_dir, "images")
    download_and_extract_images_zip(images_zip_url, images_root)

    # 3) Export annotation JSON per split
    for split, ds in ds_ann.items():
        print(f"Processing split '{split}'...")
        split_img_dir = os.path.join(dest_dir, split)
        os.makedirs(split_img_dir, exist_ok=True)

        entries = []
        for ex in ds:
            imgname = ex["imgname"]
            # move/copy the already-extracted image into split folder
            src_img = os.path.join(images_root, imgname)
            dst_img = os.path.join(split_img_dir, imgname)
            if os.path.isfile(src_img):
                shutil.copy2(src_img, dst_img)
            else:
                print(f"  Warning: image {imgname} not found in images/")

            entries.append({
                "image_id": imgname,
                "query":     ex["query"],
                "label":     ex["label"]
            })

        # write JSON
        json_path = os.path.join(dest_dir, f"{split}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Exported {len(entries)} annotations to {json_path}")

    # 4) Clean up annotation cache
    shutil.rmtree(ann_cache)
    print("Done. Annotation cache removed.")

if __name__ == "__main__":
    DEST = "/mnt/VLAI_data/unichart"
    os.makedirs(DEST, exist_ok=True)
    export_unichart(DEST)
