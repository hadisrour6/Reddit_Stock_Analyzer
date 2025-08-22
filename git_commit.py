import subprocess
from datetime import datetime

def git_push(file_path, message="Update JSON file"):
    try:
        # Stage the file
        subprocess.run(["git", "add", file_path], check=True)

        # Commit with timestamp
        commit_message = f"{message} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push to the current branch
        subprocess.run(["git", "push"], check=True)

        print("✅ File committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")

if __name__ == "__main__":
    git_push("big_movement.json", "Auto-update big_movement.json")
