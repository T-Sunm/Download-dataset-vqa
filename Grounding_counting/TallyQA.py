#!/usr/bin/env python3
import os
import subprocess
import zipfile
import shutil

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
    print(f"  ✓ Done, removed archive {zip_path}")

def main():
    base = "/mnt/VLAI_data/TallyQA"
    images_root = os.path.join(base, "images")
    coco_dir = os.path.join(images_root, "coco")
    vg_dir   = os.path.join(images_root, "visualgenome")
    qa_dir   = os.path.join(base, "qa")

    # ensure dirs
    for d in (coco_dir, vg_dir, qa_dir):
        os.makedirs(d, exist_ok=True)

    # 1) COCO train/val into coco/
    coco_urls = {
        "train2014.zip": "http://images.cocodataset.org/zips/train2014.zip",
        "val2014.zip":   "http://images.cocodataset.org/zips/val2014.zip"
    }
    for fname, url in coco_urls.items():
        zip_path = os.path.join(coco_dir, fname)
        download_with_wget(url, zip_path)
        extract_zip(zip_path, coco_dir)

    # 2) Visual Genome parts into visualgenome/
    vg_urls = {
        "images.zip":  "https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip",
        "images2.zip": "https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip"
    }
    for fname, url in vg_urls.items():
        zip_path = os.path.join(vg_dir, fname)
        download_with_wget(url, zip_path)
        extract_zip(zip_path, vg_dir)

    # 3) TallyQA JSONs into qa/
    tallyqa_url = "https://github.com/manoja328/tallyqa/raw/master/tallyqa.zip"
    tallyqa_zip = os.path.join(qa_dir, "tallyqa.zip")
    download_with_wget(tallyqa_url, tallyqa_zip)
    extract_zip(tallyqa_zip, qa_dir)

    print("\n✅ All done!")
    print(f"COCO images     → {coco_dir}")
    print(f"VisualGenome    → {vg_dir}")
    print(f"QA JSONs        → {qa_dir}")

if __name__ == "__main__":
    main()
