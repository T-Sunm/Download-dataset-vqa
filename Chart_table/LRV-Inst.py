#!/usr/bin/env python3
import os
import tarfile
import zipfile
import gdown

def download_and_extract(file_id: str, filename: str, out_dir: str):
    """
    Download file từ Google Drive theo file_id về out_dir/filename.
    - .tar.gz / .tgz: giải nén → xóa archive
    - .zip: giải nén → xóa archive
    - .json: chỉ download
    """
    os.makedirs(out_dir, exist_ok=True)
    dest_path = os.path.join(out_dir, filename)
    print(f"Downloading {filename}...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", dest_path, quiet=False)

    name = filename.lower()
    # TAR.GZ / TGZ
    if name.endswith((".tar.gz", ".tgz")):
        if not tarfile.is_tarfile(dest_path):
            print(f"{filename} không phải tar.gz hợp lệ, bỏ qua.")
            return
        print(f"Extracting {filename} …")
        with tarfile.open(dest_path, "r:gz") as tf:
            tf.extractall(path=out_dir)
        print(f"Extracted {filename}")
        os.remove(dest_path)
        print(f"Removed archive {filename}\n")

    # ZIP
    elif name.endswith(".zip"):
        try:
            with zipfile.ZipFile(dest_path, "r") as zf:
                print(f"Extracting {filename} …")
                zf.extractall(path=out_dir)
            print(f"Extracted {filename}")
            os.remove(dest_path)
            print(f"Removed archive {filename}\n")
        except zipfile.BadZipFile:
            print(f"{filename} không phải zip hợp lệ, bỏ qua.\n")

    # JSON
    elif name.endswith(".json"):
        print(f"Downloaded JSON {filename} → {out_dir}\n")

    else:
        print(f"ℹĐã download {filename} (không có thao tác tiếp) → {out_dir}\n")


def main():
    out_dir = "/mnt/VLAI_data/LRV-Inst"
    os.makedirs(out_dir, exist_ok=True)

    files = [
        ("1Dey-undzW2Nl21CYLFSkP_Y4RrfRJkYd", "images.zip"),
        ("13j2U-ectsYGR92r6J5hPdhT8T5ezItHF", "annotations.json"),
    ]

    for file_id, filename in files:
        download_and_extract(file_id, filename, out_dir)

    print("All done!")

if __name__ == "__main__":
    main()
