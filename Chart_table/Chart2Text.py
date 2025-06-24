#!/usr/bin/env python3
import os
import subprocess
import sys

def sparse_clone(repo_url: str, branch: str, subdir: str, dest: str):
    """
    Sparse‐checkout of `subdir` from `repo_url@branch` into `dest`.
    """
    os.makedirs(dest, exist_ok=True)

    cmds = [
        ["git", "init"],
        ["git", "remote", "add", "-f", "origin", repo_url],
        ["git", "config", "core.sparseCheckout", "true"],
    ]

    sparse_file = os.path.join(dest, ".git", "info", "sparse-checkout")
    os.makedirs(os.path.dirname(sparse_file), exist_ok=True)
    with open(sparse_file, "w") as f:
        # ghi đường dẫn thư mục cần checkout
        f.write(subdir.rstrip("/") + "/\n")

    cmds.append(["git", "pull", "origin", branch])

    for cmd in cmds:
        print("Running:", " ".join(cmd), "in", dest)
        subprocess.run(cmd, cwd=dest, check=True)


if __name__ == "__main__":
    REPO   = "https://github.com/vis-nlp/Chart-to-text.git"
    BRANCH = "main"
    BASE   = "/mnt/VLAI_data/Chart2Text"

    targets = {
        "pew_dataset":     "pew_dataset/dataset",
        "statista_dataset":"statista_dataset/dataset",
    }

    for folder, subpath in targets.items():
        dest = os.path.join(BASE, folder)
        print(f"\n=== Sparse‐cloning `{subpath}` → `{dest}` ===")
        try:
            sparse_clone(REPO, BRANCH, subpath, dest)
        except subprocess.CalledProcessError as e:
            print(f"ERROR cloning {subpath}: {e}", file=sys.stderr)
            sys.exit(1)

    print("\n✅ All done! Check your data under:")
    for folder in targets:
        print(f"   {os.path.join(BASE, folder, targets[folder].split('/',1)[1])}")
