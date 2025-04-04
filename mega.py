import subprocess
import os
import time
from pathlib import Path
import time

def get_path_size(path: Path) -> int:
    """
    Calculate total size of a file or directory in bytes.

    :param path: Path to the file or directory.
    :return: Total size in bytes.
    """
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
    return 0

def format_size(size_bytes: int) -> str:
    """
    Convert bytes to a human-readable format using standard units.

    :param size_bytes: Size in bytes.
    :return: Formatted string (e.g., '1.23 MB').
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


class MegaCmdInterface:
    """
    Interface for interacting with MEGA using MEGAcmd via subprocess.
    """

    def __init__(self, email: str, password: str):
        """
        Initialize the MEGA interface and log in.

        :param email: MEGA account email.
        :param password: MEGA account password.
        """
        self.email = email
        self.password = password
        self.login()

    def run_command(self, command: str):
        """
        Run a MEGAcmd command as a string using shell=True.

        :param command: The MEGAcmd command to execute as a string.
        :return: Output of the command.
        :raises Exception: If the command fails.
        """
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            if error_message:
                print(f"Command failed: {command}")
                print(f"Error output: {error_message}")
            raise Exception(f"Error: {error_message}")
        return result.stdout.strip()

    def is_logged_in(self):
        """
        Check if the user is currently logged in to MEGA.

        :return: True if logged in, False otherwise.
        """
        try:
            output = self.run_command('mega-whoami')
            return bool(output)
        except Exception:
            return False

    def login(self):
        """
        Log in to MEGA using the provided email and password.
        If already logged in, it skips re-login.
        """
        if not self.is_logged_in():
            self.run_command(f'mega-login {self.email} {self.password}')
        else:
            print("Already logged in.")

    def logout(self):
        """
        Log out of the current MEGA session, if any.
        """
        if self.is_logged_in():
            self.run_command('mega-logout')
            print("Logged out successfully.")
        else:
            print("No active session to log out from.")

    def create_folder(self, remote_path: str):
        """
        Create a new folder in MEGA.

        :param remote_path: Path of the folder to create in MEGA.
        """
        self.run_command(f'mega-mkdir "{remote_path}"')
        print(f"Folder '{remote_path}' created successfully.")

    def upload_file(self, local_path: str, remote_path: str):
        """
        Upload a local file or directory to a specified path in MEGA.

        :param local_path: Path to the local file or directory.
        :param remote_path: Destination path in MEGA.
        """
        print("🔃 Uploading...")
        start_time = time.time()
        self.run_command(f'mega-put {local_path} "{remote_path}"')
        elapsed = time.time() - start_time

        path = Path(local_path)
        size = get_path_size(path)
        readable_size = format_size(size)

        minutes, seconds = divmod(elapsed, 60)
        print(f"✅ Upload completed successfully.")
        print(f"📦 Size: {readable_size}")
        print(f"⏱ Time taken: {int(minutes)} min {int(seconds)} sec")

    def download_file(self, remote_path: str, local_path: str):
        """
        Download a file or directory from MEGA to a local path.

        :param remote_path: Path in MEGA to download from.
        :param local_path: Destination path on local filesystem.
        """
        print("🔃 Downloading...")
        start_time = time.time()
        self.run_command(f'mega-get "{remote_path}" "{local_path}"')
        elapsed = time.time() - start_time

        path = Path(local_path)
        if path.is_dir():
            downloaded_items = sorted(path.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
            if downloaded_items:
                path = downloaded_items[0]

        size = get_path_size(path)
        readable_size = format_size(size)

        minutes, seconds = divmod(elapsed, 60)
        print(f"✅ Download completed successfully.")
        print(f"📦 Size: {readable_size}")
        print(f"⏱ Time taken: {int(minutes)} min {int(seconds)} sec")

    def remove_file(self, remote_path: str):
        """
        Remove a file or folder from MEGA.

        :param remote_path: Path in MEGA to remove.
        """
        self.run_command(f'mega-rm "{remote_path}"')

    def list_files(self, remote_path: str = '/'):
        """
        List files in a MEGA directory.

        :param remote_path: Path in MEGA to list files from.
        :return: List of files in the specified directory.
        """
        output = self.run_command(f'mega-ls "{remote_path}"')
        return output.splitlines()
