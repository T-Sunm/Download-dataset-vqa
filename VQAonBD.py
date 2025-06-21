#!/usr/bin/env python3
import os
import requests
import zipfile
from tqdm import tqdm

def download_and_extract_zip(url: str, target_dir: str):
    """
    Download a ZIP archive from `url` and extract its contents under `target_dir`.
    """
    os.makedirs(target_dir, exist_ok=True)
    zip_name = os.path.basename(url)
    zip_path = os.path.join(target_dir, zip_name)
    
    # Download with progress bar
    print(f"Downloading {zip_name} …")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    with open(zip_path, "wb") as f, tqdm(
        desc=f"→ {zip_name}",
        total=total, unit="B", unit_scale=True
    ) as pbar:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    
    # Extract
    print(f"Extracting {zip_name} …")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target_dir)
    os.remove(zip_path)
    print(f"✓ Completed split at {target_dir}\n")

def main():
    base_out_dir = "/mnt/VLAI_data/VQAonBD"
    splits = {
        "train": "https://ilocr.iiit.ac.in/vqabd/assets/dataset/competition.zip",
        "val":   "https://ilocr.iiit.ac.in/vqabd/assets/dataset/competition_val.zip",
        "test":  "https://ilocr.iiit.ac.in/vqabd/assets/dataset/VQAonBD_testset.zip"
    }
    for split, url in splits.items():
        print(f"=== Processing split: {split} ===")
        split_dir = os.path.join(base_out_dir, split)
        download_and_extract_zip(url, split_dir)

if __name__ == "__main__":
    main()
