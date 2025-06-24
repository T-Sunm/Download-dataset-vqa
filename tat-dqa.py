#!/usr/bin/env python3
import os
import zipfile
import tarfile
import gdown
import shutil

def download_and_handle(file_id: str, filename: str, out_dir: str):
    """
    - Download file từ Google Drive theo file_id về out_dir/filename.
    - Nếu filename.endswith('.zip'): extract bằng zipfile rồi xóa archive.
    - Nếu filename.endswith('.tar.gz'|'.tgz'): extract bằng tarfile rồi xóa archive.
    - Nếu filename.endswith('.json'): chỉ download.
    """
    os.makedirs(out_dir, exist_ok=True)
    dest_path = os.path.join(out_dir, filename)

    print(f"Downloading {filename}...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", dest_path, quiet=False)

    ext = filename.lower()
    # ZIP
    if ext.endswith(".zip"):
        print(f"Extracting ZIP {filename} …")
        with zipfile.ZipFile(dest_path, "r") as zf:
            zf.extractall(path=out_dir)
        os.remove(dest_path)
        print(f"Removed archive {filename}\n")

    # TAR.GZ / TGZ
    elif ext.endswith((".tar.gz", ".tgz")):
        print(f"Extracting TAR.GZ {filename} …")
        with tarfile.open(dest_path, "r:gz") as tf:
            tf.extractall(path=out_dir)
        os.remove(dest_path)
        print(f"Removed archive {filename}\n")

    # JSON
    elif ext.endswith(".json"):
        print(f"Downloaded JSON {filename}\n")

    else:
        print(f"No handler for {filename}, kept as-is.\n")


def main():
    base_out_dir = "/mnt/VLAI_data/tat-dqa"
    os.makedirs(base_out_dir, exist_ok=True)

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

    for split, resources in files.items():
        split_dir = os.path.join(base_out_dir, split)
        os.makedirs(split_dir, exist_ok=True)

        for kind, file_id in resources.items():
            # Quy ước: images → .zip, annotations → .json
            if kind == "images":
                filename = f"{kind}.zip"
            else:
                filename = f"{kind}.json"
            download_and_handle(file_id, filename, split_dir)

    print("All done!")

if __name__ == "__main__":
    main()
