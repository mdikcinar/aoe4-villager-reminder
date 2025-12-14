#!/usr/bin/env python3
"""
AoE4 Villager Reminder - Automated Release Script
Fully automated GitHub release creation script
"""

import os
import sys
import re
import subprocess
import json
from pathlib import Path


def get_version():
    """Read version number from constants.py file"""
    constants_file = Path("src/utils/constants.py")
    if not constants_file.exists():
        print("[ERROR] src/utils/constants.py not found!")
        sys.exit(1)
    
    with open(constants_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        print("[ERROR] APP_VERSION not found!")
        sys.exit(1)
    
    return match.group(1)


def run_command(cmd, check=True, shell=False):
    """Run command and return result"""
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except FileNotFoundError:
        return False, "", "Command not found"


def check_dependencies():
    """Check if required tools are installed"""
    tools = {
        'git': 'Git',
        'gh': 'GitHub CLI',
        'python': 'Python'
    }
    
    missing = []
    for tool, name in tools.items():
        success, _, _ = run_command(f'{tool} --version', check=False)
        if not success:
            missing.append(name)
    
    return missing


def run_command_live(cmd, shell=False):
    """Run command and show output in real-time"""
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        result = subprocess.run(
            cmd,
            shell=shell,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def build_executable():
    """Build the executable"""
    print("\n[1/5] Building executable...")
    print("(This may take a few minutes...)\n")
    
    if os.name == 'nt':  # Windows
        success = run_command_live('build.bat', shell=True)
    else:
        # Alternative for Linux/Mac
        success = run_command_live('python -m PyInstaller build.spec --clean')
    
    if not success:
        print("[ERROR] Build failed!")
        return False
    
    exe_path = Path("dist/AoE4VillagerReminder.exe")
    if not exe_path.exists():
        print("[ERROR] Executable not created!")
        return False
    
    print(f"[OK] Executable created: {exe_path}")
    return True


def commit_changes(version):
    """Commit changes"""
    print("\n[2/5] Checking git status...")
    
    success, output, _ = run_command('git status --short', check=False)
    if success and output.strip():
        print("Changes:")
        print(output)
        
        response = input("\nDo you want to commit changes? (Y/N): ").strip().upper()
        if response == 'Y':
            commit_msg = input(f"Commit message (press Enter to use 'Release v{version}'): ").strip()
            if not commit_msg:
                commit_msg = f"Release v{version}"
            
            run_command(['git', 'add', '.'])
            success, _, error = run_command(['git', 'commit', '-m', commit_msg], check=False)
            if not success:
                print(f"[WARNING] Commit failed: {error}")
            else:
                print("[OK] Changes committed")
    else:
        print("[OK] No changes to commit")
    
    return True


def create_tag(version):
    """Create git tag"""
    print(f"\n[3/5] Creating git tag: v{version}...")
    
    tag_name = f"v{version}"
    
    # Check if tag already exists
    success, output, _ = run_command(['git', 'tag', '-l', tag_name], check=False)
    if success and output.strip():
        response = input(f"Tag {tag_name} already exists. Overwrite? (Y/N): ").strip().upper()
        if response != 'Y':
            print("[CANCELLED] Tag not created")
            return False
        run_command(['git', 'tag', '-d', tag_name], check=False)
    
    success, _, error = run_command(['git', 'tag', '-a', tag_name, '-m', f'Release {tag_name}'], check=False)
    if not success:
        print(f"[ERROR] Tag creation failed: {error}")
        return False
    
    print(f"[OK] Tag created: {tag_name}")
    return True


def push_tag(version):
    """Push tag to GitHub"""
    print(f"\n[4/5] Pushing tag to GitHub...")
    
    tag_name = f"v{version}"
    success, _, error = run_command(['git', 'push', 'origin', tag_name], check=False)
    
    if not success:
        print(f"[WARNING] Tag push failed: {error}")
        print(f"Try manually: git push origin {tag_name}")
        return False
    
    print(f"[OK] Tag pushed: {tag_name}")
    return True


def create_github_release(version):
    """Create GitHub release"""
    print(f"\n[5/5] Creating GitHub Release...")
    
    tag_name = f"v{version}"
    exe_path = Path("dist/AoE4VillagerReminder.exe")
    
    if not exe_path.exists():
        print("[ERROR] Executable not found!")
        return False
    
    # Generate release notes
    release_notes = f"""Release {tag_name}

### New Features
- See CHANGELOG.md for details

### Download
- **Windows**: Download and run AoE4VillagerReminder.exe
- No installation required, portable

### Changes
- Version {version} released
"""
    
    # Create release with GitHub CLI
    cmd = [
        'gh', 'release', 'create', tag_name,
        str(exe_path),
        '--title', tag_name,
        '--notes', release_notes
    ]
    
    success, output, error = run_command(cmd, check=False)
    
    if not success:
        if 'gh: command not found' in error or 'gh' in error.lower():
            print("[ERROR] GitHub CLI (gh) not found!")
            print("\nTo install GitHub CLI:")
            print("  Windows: winget install --id GitHub.cli")
            print("  or download from https://cli.github.com")
            print("\nAfter installation: gh auth login")
        else:
            print(f"[ERROR] Release creation failed: {error}")
            print("\nTo create release manually:")
            print(f"  1. Go to your GitHub repository")
            print(f"  2. Click on Releases tab")
            print(f"  3. Select tag: {tag_name}")
            print(f"  4. Add {exe_path} file")
        return False
    
    print(f"[OK] Release created: {tag_name}")
    
    # Find repository URL
    success, output, _ = run_command(['git', 'remote', 'get-url', 'origin'], check=False)
    if success:
        url = output.strip().replace('.git', '').replace('git@github.com:', 'https://github.com/')
        print(f"\nRelease link: {url}/releases/tag/{tag_name}")
    
    return True


def main():
    """Main function"""
    print("=" * 50)
    print("AoE4 Villager Reminder - Automated Release")
    print("=" * 50)
    
    # Read version
    version = get_version()
    print(f"\nCurrent version: {version}")
    
    # Get confirmation
    response = input(f"\nDo you want to create a release with this version? (Y/N): ").strip().upper()
    if response != 'Y':
        print("Release cancelled.")
        sys.exit(0)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n[WARNING] Missing tools: {', '.join(missing)}")
        if 'GitHub CLI' in missing:
            print("Cannot create release without GitHub CLI, but tag can be created.")
            response = input("Continue anyway? (Y/N): ").strip().upper()
            if response != 'Y':
                sys.exit(0)
    
    # Run steps
    steps = [
        build_executable,
        lambda: commit_changes(version),
        lambda: create_tag(version),
        lambda: push_tag(version),
        lambda: create_github_release(version)
    ]
    
    for step in steps:
        if not step():
            print("\n[WARNING] A step failed, but continuing...")
    
    print("\n" + "=" * 50)
    print("Release process completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
