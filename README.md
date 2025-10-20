# Release Automation PoC

This is a proof of concept for automating release branch creation using GitHub Actions and Python.

## 🚀 How to Use

1. Fork this repo or upload to your own GitHub account.
2. Go to **Settings → Secrets → Actions** and add a secret:
   - `GITHUB_TOKEN` = your personal access token (with repo scope)
3. Go to **Actions → Create Release Branch → Run workflow**
4. Enter a release date (e.g. `2025-11-15`).
5. The workflow will compute branch name and create it automatically.

## ⚙️ Configuration

Edit `config/settings.yaml` to match your repo details.
When moving to Bitbucket, change:
- `repo_type: bitbucket`
- Update `bitbucket:` section with your workspace and repo slug.
