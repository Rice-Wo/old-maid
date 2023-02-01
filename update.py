import os
import shutil
import zipfile
import requests
import subprocess
import json

with open('setting.json', 'r', encoding = "utf-8") as setting:
	setting = json.load(setting)

def check_update():
    # Make a request to the GitHub API to check for updates
    response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases/latest")
    latest_release = response.json()
    latest_version = latest_release["tag_name"]

    # Compare the latest version to the current version
    current_version = setting['version']
    if latest_version > current_version:
        return latest_release["zipball_url"]
    else:
        return None

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
    
    # Find the location of the updated files
    update_folder = [f for f in os.listdir("update") if os.path.isdir(os.path.join("update", f))][0]
    update_folder = os.path.join("update", update_folder)
    

    # Copy all files from the update folder to the current folder
    for file in os.listdir(update_folder):
        new_file_path = os.path.join(update_folder, file)
        old_file_path = os.path.join(".", file)
        if os.path.isfile(new_file_path):
            if not os.path.exists(old_file_path):
                os.makedirs(os.path.dirname(old_file_path), exist_ok=True)
            shutil.copy2(new_file_path, old_file_path)

    # Clean up the update folder
    shutil.rmtree("update")
    os.remove(file_path)

    # Re-run the main program
    subprocess.run(["python3", "Rice_Wo_Maid.py"])

# Example usage
update_url = check_update()
if update_url:
    download_update(update_url)
    apply_update("update.zip")
    print("success")
else:
    print("The software is already up to date.")
