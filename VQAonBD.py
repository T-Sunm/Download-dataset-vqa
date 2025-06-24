#!/usr/bin/env python3
import os
import subprocess
import zipfile
import sys

def download_with_wget(url: str, dest_path: str):
    """
    Download a remote file via wget -c into dest_path, with resume support.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    cmd = ["wget", "-c", url, "-O", dest_path]
    print(f"Downloading with wget: {url}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        sys.exit(1)

def download_and_extract_zip(url: str, target_dir: str):
    """
    Download a ZIP via wget, extract it into target_dir, then remove the ZIP.
    """
    os.makedirs(target_dir, exist_ok=True)
    zip_name = os.path.basename(url)
    zip_path = os.path.join(target_dir, zip_name)

    # 1) Download via wget
    download_with_wget(url, zip_path)

    # 2) Extract
    print(f"Extracting {zip_name} → {target_dir}")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(target_dir)
    except zipfile.BadZipFile:
        print(f"Bad zip file: {zip_path}", file=sys.stderr)
        sys.exit(1)

    # 3) Clean up
    os.remove(zip_path)
    print(f"✔ Completed split at {target_dir}\n")

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

    print("All splits downloaded and extracted.")

if __name__ == "__main__":
    main()
