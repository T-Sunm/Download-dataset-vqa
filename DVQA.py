#!/usr/bin/env python3
import os
import tarfile
import shutil
import gdown

def download_and_extract(file_id, filename, out_dir):
    output_path = os.path.join(out_dir, filename)
    print(f"Downloading {filename}...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)
    # Kiểm tra xem có phải tar.gz hợp lệ không
    if not tarfile.is_tarfile(output_path):
        print(f"{filename} không phải tar.gz hợp lệ, bỏ qua.")
        return
    print(f"Extracting {filename}...")
    with tarfile.open(output_path, mode="r:gz") as tf:
        tf.extractall(path=out_dir)
    print(f"Đã giải nén {filename}")
    os.remove(output_path)
    print(f"Đã xóa archive {filename}\n")

def main():
    out_dir = "/mnt/VLAI_data/DVQA"
    os.makedirs(out_dir, exist_ok=True)

    files = [
        ("1iKH2lTi1-QxtNUVRxTUWFvUvRHq6HAsZ", "images.tar.gz"),
        ("18SJ13V4qEt1ixOQPbRmEnZKQrjS5v14T", "qa.tar.gz"),
        ("1vBz8Ji4TMY7rzTL2_DJCTUEyWR7l16W6", "metadata.tar.gz")
    ]

    for file_id, file_name in files:
        download_and_extract(file_id, file_name, out_dir)

if __name__ == "__main__":
    main()
