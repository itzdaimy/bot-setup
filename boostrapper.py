import os
import requests
import json

VERSION_URL = "https://raw.githubusercontent.com/itzdaimy/bot-setup/refs/heads/main/version.json"
FILES_TO_DOWNLOAD = {
    "api/setup.py": "https://raw.githubusercontent.com/itzdaimy/bot-setup/refs/heads/main/api/setup.py",
    "features/example.py": "https://raw.githubusercontent.com/itzdaimy/bot-setup/refs/heads/main/features/example.py",
    "main.py": "https://raw.githubusercontent.com/itzdaimy/bot-setup/refs/heads/main/main.py",
    ".env": "https://raw.githubusercontent.com/itzdaimy/bot-setup/refs/heads/main/.env"
}

def create_folder_if_not_exists(folder_path):
    if folder_path and not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

def create_bin_folder():
    create_folder_if_not_exists("bin")

def check_local_version():
    version_file = "bin/version.json"
    if os.path.exists(version_file):
        with open(version_file, "r") as file:
            data = json.load(file)
            return data.get("version")
    return None

def update_local_version(version):
    version_data = {"version": version}
    with open("bin/version.json", "w") as file:
        json.dump(version_data, file)
    print(f"Local version updated to {version} in 'bin/version.json'.")

def get_github_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        github_version = response.json().get("version")
        print(f"GitHub version: {github_version}")
        return github_version
    except Exception as e:
        print(f"Error fetching version from GitHub: {e}")
        return None

def download_files(file_dict):
    for filepath, url in file_dict.items():
        folder = os.path.dirname(filepath)
        create_folder_if_not_exists(folder)
        print(f"Downloading {filepath} from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, "wb") as file:
                file.write(response.content)
            print(f"Downloaded {filepath} successfully.")
        else:
            print(f"Failed to download {filepath}. HTTP Status: {response.status_code}")

def reinstall_files_if_needed():
    github_version = get_github_version()
    local_version = check_local_version()

    if not github_version:
        print("Failed to get GitHub version. Exiting...")
        return

    if local_version != github_version:
        print(f"Version mismatch. Local version: {local_version}, GitHub version: {github_version}")
        print("Reinstalling files...")
        download_files(FILES_TO_DOWNLOAD)
        update_local_version(github_version)
    else:
        print("Versions match. No update required.")

if __name__ == "__main__":
    create_bin_folder()
    reinstall_files_if_needed()
    input("Press Enter to exit...")