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

    # 1) Download với progress bar
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

    # 2) Giải nén
    print(f"Extracting {zip_name} → {target_dir}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(target_dir)

    # 3) Xóa file ZIP
    os.remove(zip_path)
    print(f"✔ Done, removed archive {zip_name}\n")

def main():
    DEST = "/mnt/VLAI_data/OODVQA"
    os.makedirs(DEST, exist_ok=True)

    zip_url = (
        "https://huggingface.co/datasets/PahaII/vllm_safety_evaluation/"
        "resolve/main/safety_evaluation_benchmark_datasets.zip"
    )
    download_and_extract_zip(zip_url, DEST)

if __name__ == "__main__":
    main()
