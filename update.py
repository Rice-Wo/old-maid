import os
import shutil
import zipfile
import requests
import subprocess
import logging.config
import json

with open('log_config.json', "r", encoding='utf-8') as f:
    log = json.load(f)
logging.config.dictConfig(log)
logger = logging.getLogger()


response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases/latest")
latest_release = response.json()
url = latest_release["zipball_url"]

def download_update(url):
    # Download the update file
    response = requests.get(url)
    with open("update.zip", "wb") as f:
        f.write(response.content)

def apply_update(file_path):
    # Close the main program
    subprocess.run(["pkill", "Rice_Wo_Maid.py"])

    # Unzip the update file
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall("update")

    # Copy all files from the update folder to the current folder
    for root, dirs, files in os.walk("update"):
        for file in files:
            new_file_path = os.path.join(root, file)
            old_file_path = os.path.join(".", os.path.relpath(new_file_path, "update"))
            shutil.copy2(new_file_path, old_file_path)

    # Clean up the update folder
    shutil.rmtree("update")
    os.remove(file_path)

    # Re-run the main program
    subprocess.run(["python3", "Rice_Wo_Maid.py"])

# Example usage
logging.info('file update start')
download_update(url)
apply_update("update.zip")
logging.info("file update success")