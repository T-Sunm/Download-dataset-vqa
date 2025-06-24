#!/usr/bin/env python3
import os
import json
import shutil
from datasets import load_dataset

def export_robut(dest_root: str):
    # 1) Load dataset vào cache
    cache_dir = "/mnt/VLAI_data/Chart2Text/cached"
    ds = load_dataset("yilunzhao/robut", cache_dir=cache_dir)

    # 2) Với mỗi split, tạo folder con và xuất data
    for split in ds:
        print(f"Processing split '{split}' ({len(ds[split])} samples)…")
        split_dir   = os.path.join(dest_root, split)
        images_dir  = os.path.join(split_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        ann_list = []

        for sample in ds[split]:
            sid = sample["id"]
            # 2a) ghi file images/<id>.json
            tbl = sample["table"]
            with open(os.path.join(images_dir, f"{sid}.json"), "w", encoding="utf-8") as f:
                json.dump({"id": sid, "table": tbl}, f, ensure_ascii=False)

            # 2b) gom annotation cho split
            ann_list.append({
                "id":                sid,
                "question":          sample["question"],
                "answers":           sample["answers"],
                "perturbation_type": sample["perturbation_type"],
                "original_id":       sample["original_id"]
            })

        # 3) Viết annotation.json cho split
        ann_path = os.path.join(split_dir, "annotation.json")
        with open(ann_path, "w", encoding="utf-8") as f:
            json.dump(ann_list, f, ensure_ascii=False, indent=2)
        print(f"  → saved {len(ann_list)} annotations → {ann_path}")

    # 4) Xóa cache
    shutil.rmtree(cache_dir)
    print(f"Removed cache at {cache_dir}")

if __name__ == "__main__":
    DEST = "/mnt/VLAI_data/Chart2Text/robut"
    os.makedirs(DEST, exist_ok=True)
    export_robut(DEST)
