#!/usr/bin/env python3
import os
import gdown

def main():
    FOLDER_ID = "1ituEWZ5F7G9T9AZ0kzZZLrHNhRigHCZJ"
    DEST = "/mnt/VLAI_data/MultiHiertt"
    os.makedirs(DEST, exist_ok=True)

    url = f"https://drive.google.com/drive/folders/{FOLDER_ID}"
    print(f"Downloading folder {FOLDER_ID} into {DEST} …")
    gdown.download_folder(url, output=DEST, quiet=False, use_cookies=False)

    print("All done!")

if __name__ == "__main__":
    main()
