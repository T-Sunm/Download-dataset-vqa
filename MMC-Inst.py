import os
import tarfile
import shutil

src_dir = "/home/minhtq/workspace/Download-dataset-vqa/MMC-Inst"
dst_dir = "/mnt/VLAI_data/MMC-Inst"
os.makedirs(dst_dir, exist_ok=True)

for fn in os.listdir(src_dir):
    src_path = os.path.join(src_dir, fn)
    dst_path = os.path.join(dst_dir, fn)

    if fn.lower().endswith((".tar.gz", ".tgz")):
        # Mở và extract
        with tarfile.open(src_path, mode="r:gz") as tf:
            tf.extractall(path=dst_dir)
            print(f"✅  Đã giải nén {fn} → {dst_dir}")
    elif fn.lower().endswith(".json"):
        # Di chuyển file JSON
        shutil.move(src_path, dst_path)
        print(f"✅  Đã di chuyển {fn} → {dst_dir}")


