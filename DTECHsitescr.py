import os
import subprocess
import shutil

def authenticate_github():
    """Authenticate GitHub account if not already linked."""
    print("\n🔍 Checking GitHub authentication...")
    result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ GitHub account already authenticated!")
    else:
        print("⚠️ GitHub account not linked. Let's authenticate.")
        # Allow interactive GitHub authentication
        auth_result = subprocess.run(['gh', 'auth', 'login'])
        if auth_result.returncode == 0:
            print("✅ GitHub account linked successfully!")
        else:
            print("❌ Authentication failed. Please try again.")
            exit(1)

def create_repo(repo_name):
    print(f"\n🚀 Creating GitHub repository '{repo_name}'...")
    result = subprocess.run(['gh', 'repo', 'create', repo_name, '--public', '--confirm'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Repository '{repo_name}' created successfully!")
    else:
        print(f"❌ Error creating repository: {result.stderr}")
        exit(1)

def clone_repo(username, repo_name):
    print(f"\n📂 Cloning the repository '{repo_name}'...")
    result = subprocess.run(['git', 'clone', f'https://github.com/{username}/{repo_name}.git'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Repository cloned successfully!")
    else:
        print(f"❌ Error cloning repository: {result.stderr}")
        exit(1)

def copy_files(website_path, repo_name):
    print(f"\n📤 Copying website file from '{website_path}'...")
    if os.path.isfile(website_path):
        destination_path = os.path.join(f'./{repo_name}', 'index.html')
        shutil.copy(website_path, destination_path)
        print("✅ File copied and renamed to 'index.html'")
    else:
        print(f"❌ Error: File '{website_path}' does not exist.")
        exit(1)

def commit_and_push(repo_name):
    os.chdir(repo_name)
    print("\n🔗 Committing and pushing changes to GitHub...")
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit - Added website files'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("✅ Changes pushed to GitHub successfully!")

def enable_github_pages(username, repo_name):
    print("\n🌐 Enabling GitHub Pages...")
    result = subprocess.run([
        'gh', 'api', f'/repos/{username}/{repo_name}/pages',
        '-X', 'POST',
        '-H', 'Accept: application/vnd.github+json',
        '-f', 'source[branch]=main',
        '-f', 'source[path]=/'
    ], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ GitHub Pages enabled successfully!")
        print(f"🌟 Your site is live at: https://{username}.github.io/{repo_name}/")
    else:
        print(f"❌ Error enabling GitHub Pages: {result.stderr}")
        exit(1)

def main():
    print("\n🔷 Welcome to the **D-TECH GitHub Pages Tool** 🔷")
    
    # Step 1: Authenticate GitHub account
    authenticate_github()
    
    # Step 2: Gather user input
    username = input("\n🔹 Enter your GitHub username (e.g., preasx24): ")
    repo_name = input("🔹 Enter the name of your repository (e.g., DTECH-SERVICES): ")
    
    # Step 3: Create the GitHub repository
    create_repo(repo_name)

    # Step 4: Clone the repository
    clone_repo(username, repo_name)

    # Step 5: Ask for the website file location
    website_path = input("\n🔹 Enter the path to your website file (e.g., /storage/emulated/0/Download/Telegram/amazon.html): ")

    # Step 6: Copy the file to the repository
    copy_files(website_path, repo_name)

    # Step 7: Commit and push the changes
    commit_and_push(repo_name)

    # Step 8: Enable GitHub Pages
    enable_github_pages(username, repo_name)

    print("\n🎉 Setup Complete! Your website is now live. Thank you for using the D-TECH GitHub Pages Tool! 🎉")

if __name__ == "__main__":
    main()
