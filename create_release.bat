@echo off
setlocal enabledelayedexpansion
REM AoE4 Villager Reminder - Release Creation Script
REM This script helps create a GitHub release

echo ========================================
echo AoE4 Villager Reminder - Release Helper
echo ========================================
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found! Please install Git.
    pause
    exit /b 1
)

REM Read version from constants.py
for /f "tokens=3 delims== " %%a in ('findstr "APP_VERSION" src\utils\constants.py') do (
    set VERSION=%%a
    set VERSION=!VERSION:"=!
    set VERSION=!VERSION: =!
)
echo Current version: %VERSION%
echo.

REM Ask for confirmation
set /p CONFIRM="Do you want to create a release with this version? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Release cancelled.
    pause
    exit /b 0
)

echo.
echo [1/5] Building executable...
call build.bat
if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [2/5] Checking git status...
git status --short
echo.
set /p COMMIT="Do you want to commit changes? (Y/N): "
if /i "%COMMIT%"=="Y" (
    set /p COMMIT_MSG="Commit message (press Enter to use 'Release v%VERSION%'): "
    if "!COMMIT_MSG!"=="" set COMMIT_MSG=Release v%VERSION%
    git add .
    git commit -m "!COMMIT_MSG!"
)

echo.
echo [3/5] Creating git tag...
set TAG_NAME=v%VERSION%
git tag -a %TAG_NAME% -m "Release %TAG_NAME%"
if errorlevel 1 (
    echo [WARNING] Tag may already exist. Continuing...
)

echo.
echo [4/5] Pushing tag to GitHub...
git push origin %TAG_NAME%
if errorlevel 1 (
    echo [WARNING] Tag push failed. Try manually: git push origin %TAG_NAME%
)

echo.
echo [5/5] Creating GitHub Release...
REM Check if GitHub CLI is available
gh --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] GitHub CLI (gh) not found!
    echo.
    echo To install GitHub CLI:
    echo   winget install --id GitHub.cli
    echo   or download from https://cli.github.com
    echo.
    echo To create release manually:
    echo   1. Go to your GitHub repository
    echo   2. Click on Releases tab
    echo   3. Click "Draft a new release" button
    echo   4. Select tag: %TAG_NAME%
    echo   5. Add dist\AoE4VillagerReminder.exe file
    echo   6. Write release notes and publish
    echo.
    echo Or after installing GitHub CLI:
    echo   gh release create %TAG_NAME% dist\AoE4VillagerReminder.exe --title "%TAG_NAME%" --notes "Release %TAG_NAME%"
) else (
    REM Check if executable exists
    if not exist "dist\AoE4VillagerReminder.exe" (
        echo [ERROR] Executable not found: dist\AoE4VillagerReminder.exe
        echo Check the build process.
    ) else (
        REM Create release with GitHub CLI
        echo Creating release notes...
        REM Create temporary release notes file
        (
            echo Release %TAG_NAME%
            echo.
            echo ### New Features
            echo - See CHANGELOG.md for details
            echo.
            echo ### Download
            echo - **Windows**: Download and run AoE4VillagerReminder.exe
            echo - No installation required, portable
        ) > release_notes_temp.txt
        
        gh release create %TAG_NAME% "dist\AoE4VillagerReminder.exe" --title "%TAG_NAME%" --notes-file release_notes_temp.txt
        del release_notes_temp.txt
        
        if errorlevel 1 (
            echo [ERROR] Release creation failed!
            echo GitHub CLI authentication may be required: gh auth login
        ) else (
            echo.
            echo ========================================
            echo [SUCCESS] Release created!
            echo ========================================
            echo.
            echo Release link: https://github.com/yourusername/aoe4-villager-reminder/releases/tag/%TAG_NAME%
            echo.
        )
    )
)

echo.
pause
