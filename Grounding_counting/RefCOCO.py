#!/usr/bin/env python3
import os
import subprocess
import zipfile
import sys

def download_with_wget(url: str, dest_path: str):
    """Download via wget -c (resume support)."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    cmd = ["wget", "-c", url, "-O", dest_path]
    print(f"Downloading {url} → {dest_path}")
    subprocess.run(cmd, check=True)

def extract_zip(zip_path: str, extract_to: str):
    """Extract a ZIP archive and remove it."""
    print(f"Extracting {os.path.basename(zip_path)} → {extract_to}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    os.remove(zip_path)
    print(f"  ✓ Removed archive {zip_path}")

def main():
    base = "/mnt/VLAI_data/RefCOCO"
    data_dir   = os.path.join(base, "data")
    images_dir = os.path.join(base, "images", "mscoco")

    # 1) Tạo thư mục cần thiết
    for d in (data_dir, images_dir):
        os.makedirs(d, exist_ok=True)

    # 2) Download & extract RefCOCO datasets
    cleaned = {
        "refcoco.zip":   "https://web.archive.org/web/20220413011718/https://bvisionweb1.cs.unc.edu/licheng/referit/data/refcoco.zip",
        "refcoco+.zip":  "https://web.archive.org/web/20220413011656/https://bvisionweb1.cs.unc.edu/licheng/referit/data/refcoco+.zip",
        "refcocog.zip":  "https://web.archive.org/web/20220413012904/https://bvisionweb1.cs.unc.edu/licheng/referit/data/refcocog.zip",
    }
    for fname, url in cleaned.items():
        zip_path = os.path.join(data_dir, fname)
        download_with_wget(url, zip_path)
        extract_zip(zip_path, data_dir)

    # 3) Download & extract COCO train2014 into images/mscoco/train2014
    coco_url = "http://images.cocodataset.org/zips/train2014.zip"
    coco_zip = os.path.join(images_dir, "train2014.zip")
    download_with_wget(coco_url, coco_zip)
    extract_zip(coco_zip, images_dir)

    print("\n✅ All done!")
    print("Data folders:")
    print("  - RefCOCO data →", data_dir)
    print("  - COCO images  →", images_dir)

if __name__ == "__main__":
    main()
