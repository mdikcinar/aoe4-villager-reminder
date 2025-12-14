# 🚀 GitHub Release Guide

This document explains how to create GitHub releases for the AoE4 Villager Reminder project.

## ⚡ Automated Release (Recommended)

The easiest way! Automate the entire process with a single command:

### Python Script (Cross-Platform)

```bash
python create_release.py
```

### Windows Batch Script

```bash
create_release.bat
```

These scripts automatically:
1. ✅ Read the version number
2. ✅ Build the executable
3. ✅ Commit git changes (optional)
4. ✅ Create git tag
5. ✅ Push tag to GitHub
6. ✅ Create GitHub release (with GitHub CLI)

**Requirements:**
- Git
- GitHub CLI (`gh`) - [Install](https://cli.github.com)
- GitHub CLI authentication: `gh auth login`

---

## 📋 Manual Release Creation Steps

### 1. Update Version Number

Update the version number before releasing:

```bash
# Update APP_VERSION in src/utils/constants.py
# Example: "1.0.0" → "1.0.1" or "1.1.0"
```

### 2. Build Executable

```bash
# On Windows, run build.bat
build.bat

# Or manually:
pyinstaller build.spec --clean
```

After the build completes, `dist/AoE4VillagerReminder.exe` will be created.

### 3. Create Git Tag and Push

```bash
# Commit changes (if you haven't already)
git add .
git commit -m "Release v1.0.0"

# Create tag (based on version number)
git tag -a v1.0.0 -m "Release v1.0.0"

# Push tag to GitHub
git push origin v1.0.0

# Also push main branch
git push origin main
```

### 4. Create Release on GitHub

#### Method 1: GitHub Web Interface (Recommended)

1. Go to your GitHub repository
2. Click on the **Releases** tab (on the right side)
3. Click **"Create a new release"** or **"Draft a new release"** button
4. **Tag version**: Select `v1.0.0` (or create a new tag)
5. **Release title**: `v1.0.0` or `Release v1.0.0`
6. Write release notes in the **Description** section (you can use the template below)
7. **Attach binaries**: Drag and drop `dist/AoE4VillagerReminder.exe` file
8. Click **"Publish release"** button

#### Method 2: GitHub CLI (gh)

```bash
# Create release with GitHub CLI
gh release create v1.0.0 dist/AoE4VillagerReminder.exe \
  --title "v1.0.0" \
  --notes "Release v1.0.0 - First stable release"
```

### 5. Release Notes Template

```markdown
## 🎉 Release v1.0.0

### ✨ New Features
- First stable release
- API and Manual mode support
- Multi-language support (TR, EN, DE, ES, FR)
- Statistics tracking

### 🐛 Fixes
- [Add bug fixes here if any]

### 📝 Changes
- [Add breaking changes here if any]

### 📥 Download
- **Windows**: Download and run `AoE4VillagerReminder.exe`
- No installation required, portable

### 🔗 Links
- [README](README.md)
- [Report Issue](https://github.com/yourusername/aoe4-villager-reminder/issues)
```

## 🔄 Quick Release Commands

### Automated (Recommended)

```bash
# Python script (all platforms)
python create_release.py

# Or Windows batch script
create_release.bat
```

### Manual

```bash
# 1. Build
build.bat

# 2. Create tag and push
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 3. Create release with GitHub CLI
gh release create v1.0.0 dist/AoE4VillagerReminder.exe --title "v1.0.0" --notes "Release v1.0.0"
```

## 📌 Important Notes

- ✅ Update version number before each release
- ✅ Test the executable file
- ✅ Write detailed release notes
- ✅ Keep tag names in `v1.0.0` format (semantic versioning)
- ✅ Don't forget to push the main branch as well

## 🏷️ Semantic Versioning

Version numbers follow `MAJOR.MINOR.PATCH` format:

- **MAJOR**: Breaking changes (e.g., 1.0.0 → 2.0.0)
- **MINOR**: New features, backward compatible (e.g., 1.0.0 → 1.1.0)
- **PATCH**: Bug fixes (e.g., 1.0.0 → 1.0.1)
