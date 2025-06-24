# tham khảo tại: https://github.com/orgs/community/discussions/102639
#!/usr/bin/env python3
import os
import subprocess
import sys

def sparse_clone(repo_url: str, branch: str, subdir: str, dest: str):
    """
    Perform a sparse-checkout of `subdir` from `repo_url@branch` into `dest`.
    """
    # 1) Chuẩn bị thư mục đích
    os.makedirs(dest, exist_ok=True)

    # 2) Init repo & add remote
    cmds = [
        ["git", "init"],
        ["git", "remote", "add", "-f", "origin", repo_url],
        ["git", "config", "core.sparseCheckout", "true"],
    ]
    # 3) Viết sparse-checkout pattern
    sparse_file = os.path.join(dest, ".git", "info", "sparse-checkout")
    os.makedirs(os.path.dirname(sparse_file), exist_ok=True)
    with open(sparse_file, "w") as f:
        # Ghi chính xác thư mục bạn cần
        f.write(subdir.rstrip("/") + "/\n")

    # 4) Pull branch
    cmds.append(["git", "pull", "origin", branch])

    # 5) Thực thi
    for cmd in cmds:
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, cwd=dest, check=True)

if __name__ == "__main__":
    repo      = "https://github.com/lupantech/PromptPG.git"
    branch    = "main"
    subfolder = "data/tabmwp"
    dest_dir  = "/mnt/VLAI_data/TabMWP"

    try:
        sparse_clone(repo, branch, subfolder, dest_dir)
        print(f"Sparse-checkout complete! Check files in `{dest_dir}/{subfolder}`")
    except subprocess.CalledProcessError as e:
        print("Error during git operation:", e, file=sys.stderr)
        sys.exit(1)

