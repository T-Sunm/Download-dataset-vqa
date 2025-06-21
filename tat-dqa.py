#!/usr/bin/env python3
import os
import tarfile
import gdown
import shutil

def download_and_handle(file_id: str, filename: str, out_dir: str):
    """
    - Download file từ Google Drive theo file_id, lưu về out_dir/filename.
    - Nếu filename.endswith('.tar.gz'|' .tgz'): extract rồi xóa file nén.
    - Nếu filename.endswith('.json'): chỉ download.
    """
    os.makedirs(out_dir, exist_ok=True)
    dest_path = os.path.join(out_dir, filename)

    print(f"Downloading {filename}...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", dest_path, quiet=False)

    ext = filename.lower()
    if ext.endswith((".tar.gz", ".tgz")):
        print(f"Extracting {filename} into {out_dir}...")
        with tarfile.open(dest_path, mode="r:gz") as tf:
            tf.extractall(path=out_dir)
        print(f"Extracted {filename}")
        os.remove(dest_path)
        print(f"Removed archive {filename}\n")

    elif ext.endswith(".json"):
        print(f"Downloaded JSON {filename} → {out_dir}\n")

    else:
        print(f"ℹDownloaded {filename} (no further action) → {out_dir}\n")


def main():
    base_out_dir = "/mnt/VLAI_data/tat-dqa"
    os.makedirs(base_out_dir, exist_ok=True)

    # Định nghĩa file IDs (có thể mở rộng để bao gồm JSON nếu cần)
    files = {
        "train": {
            "images":      "1VX4U0wx4ojITs72d5FAKvNJMkL5J6Xdw",
            "annotations": "1FQUbZRlJKB-1sbvZ_HiZtE5isNwSvjki",
        },
        "dev": {
            "images":      "1M1CtHAS4SzFFnNVsFVGgpaGq84mEzPcR",
            "annotations": "1dmXKledPa6ptXuFibUCtoJMEP6oCD60N",
        },
        "test": {
            "images":      "1iqe5r-qgQZLhGtM4G6LkNp9S6OCwOF2L",
            "annotations": "1Dqvlu83R4t5odayhtt65qwFkxHWmieOr",
        },
    }

    # Thực hiện cho từng split
    for split, resources in files.items():
        split_dir = os.path.join(base_out_dir, split)
        os.makedirs(split_dir, exist_ok=True)

        for kind, file_id in resources.items():
            ext = "json" if kind in ["annotations", "qa"] else "tar.gz"
            filename = f"{kind}.{ext}"
            download_and_handle(file_id, filename, split_dir)

    print("All done!")

if __name__ == "__main__":
    main()
