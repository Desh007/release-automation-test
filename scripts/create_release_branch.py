import os
import sys
import yaml
import requests
from datetime import datetime

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def get_latest_release_branch(headers, config):
    url = f"{config['github']['api_url']}/repos/{config['github']['owner']}/{config['github']['repo']}/branches"
    resp = requests.get(url, headers=headers)
    branches = [b["name"] for b in resp.json()]
    release_branches = [b for b in branches if b.startswith(config["release_prefix"])]
    if not release_branches:
        print("⚠️ No release branches found. Using base branch.")
        return config["base_branch"], datetime.today()
    latest_branch = sorted(release_branches)[-1]
    date_str = latest_branch.replace(config["release_prefix"], "").split("_")[0]
    last_date = datetime.strptime(date_str, "%Y%m%d")
    return latest_branch, last_date

def create_new_branch(branch_name, base_branch, headers, config):
    ref_url = f"{config['github']['api_url']}/repos/{config['github']['owner']}/{config['github']['repo']}/git/ref/heads/{base_branch}"
    ref_resp = requests.get(ref_url, headers=headers)
    if ref_resp.status_code != 200:
        print(f"❌ Failed to fetch base branch info: {ref_resp.text}")
        return
    sha = ref_resp.json()["object"]["sha"]

    create_url = f"{config['github']['api_url']}/repos/{config['github']['owner']}/{config['github']['repo']}/git/refs"
    payload = {"ref": f"refs/heads/{branch_name}", "sha": sha}
    resp = requests.post(create_url, headers=headers, json=payload)
    if resp.status_code == 201:
        print(f"✅ Branch '{branch_name}' created successfully.")
    else:
        print(f"❌ Failed to create branch: {resp.text}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_release_branch.py <YYYY-MM-DD>")
        sys.exit(1)

    target_date_str = sys.argv[1]
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")

    config = load_config()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"}

    last_branch, last_date = get_latest_release_branch(headers, config)
    days_diff = (target_date - last_date).days

    new_branch = f"{config['release_prefix']}{target_date.strftime('%Y%m%d')}_D{days_diff}"
    print(f"🧮 New branch name: {new_branch}")

    auto_approve = os.getenv("AUTO_APPROVE", "true").lower()
    if auto_approve not in ["y", "yes", "true"]:
        print("❌ Approval denied. Exiting.")
        return

    print(f"✅ Approval granted automatically for: {', '.join(config['approvers'])}")
    create_new_branch(new_branch, config["base_branch"], headers, config)

if __name__ == "__main__":
    main()
