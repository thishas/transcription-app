# GitHub Setup Knowledge Base

## Git Installation Guide

### Git Setup Options (Windows)

1. **Default Editor**
   - Select "Use Notepad++ as Git's default editor"
   - Avoid VS Code option if Next button is unavailable

2. **Initial Branch Name**
   - Select "Override the default branch name for new repositories"
   - Set to "main"
   - This matches GitHub's default branch naming

3. **PATH Environment**
   - Select "Git from the command line and also from 3rd-party software"
   - Recommended option for best compatibility
   - Works with all development tools

4. **SSH Executable**
   - Select "Use bundled OpenSSH"
   - Comes pre-packaged with Git
   - Best compatibility with GitHub

5. **HTTPS Transport Backend**
   - Select "Use the OpenSSL library"
   - Standard SSL/TLS library for Git
   - Best for GitHub compatibility

6. **Line Ending Conversions**
   - Select "Checkout Windows-style, commit Unix-style line endings"
   - Best for cross-platform compatibility
   - Handles CRLF/LF automatically

7. **Terminal Emulator**
   - Select "Use MinTTY (the default terminal of MSYS2)"
   - Better Unicode support
   - Resizable window and better features

8. **Default `git pull` Behavior**
   - Select "Fast-forward or merge"
   - Most flexible option
   - Best for collaboration

9. **Credential Helper**
   - Select "Git Credential Manager"
   - Secure credential management
   - Better GitHub integration

10. **Extra Options**
    - Enable both:
      - File system caching (performance boost)
      - Symbolic links (additional features)

## GitHub Repository Setup Steps

1. **Create GitHub Account** (if not already done)
   - Visit github.com
   - Sign up with your email
   - Verify email address

2. **Create New Repository**
   - Click "+" in top right
   - Select "New repository"
   - Name: "transcription-app"
   - Description: "Real-time English to Spanish speech transcription and translation"
   - Make it Public
   - Don't initialize with README (we have one)

3. **First-Time Git Setup**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

4. **Initialize Local Repository**
```bash
cd C:/Users/thish/CascadeProjects/transcription-app
git init
git add .
git commit -m "Initial commit: English to Spanish Transcription App"
```

5. **Link to GitHub**
```bash
git remote add origin https://github.com/thishas/transcription-app.git
git branch -M main
git push -u origin main
```

## Important Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push

# Pull changes
git pull

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout branch-name
```

## Best Practices

1. **Commit Messages**
   - Use clear, descriptive messages
   - Start with verb (Add, Update, Fix, etc.)
   - Keep under 50 characters if possible

2. **Branching**
   - Create feature branches for new features
   - Use bugfix branches for fixes
   - Keep main branch stable

3. **Pushing/Pulling**
   - Pull before starting new work
   - Push regularly to backup changes
   - Resolve conflicts promptly

4. **Security**
   - Never commit sensitive data
   - Use .gitignore for private files
   - Keep credentials secure

## Troubleshooting

1. **Authentication Issues**
   - Check Git Credential Manager
   - Verify GitHub tokens
   - Ensure correct remote URL

2. **Push/Pull Errors**
   - Pull latest changes first
   - Check branch names
   - Verify internet connection

3. **Line Ending Issues**
   - Check core.autocrlf setting
   - Use .gitattributes if needed
   - Don't change line ending settings mid-project
