import datetime
import re
import subprocess
import argparse
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")

# =============== CONFIG ===============
# Default start date of your 100-day challenge
CHALLENGE_START = datetime.date(2025, 9, 7)  # <-- change this to your real start date
# ======================================

def get_today_day(start_date):
    """Calculate which Day number today is based on start_date"""
    today = datetime.date.today()
    delta = (today - start_date).days + 1
    return max(1, delta)  # at least Day 1

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Daily Issue Helper for 100 Days Challenge")
    parser.add_argument("--manual", type=int, help="Manually pick a specific Day number (1–100)")
    args = parser.parse_args()

    # Step 1: Connect to GitHub
    g = Github(TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Step 2: Decide which day to use
    if args.manual:
        day_num = args.manual
        print(f"📌 Manual mode → Day {day_num}")
    else:
        day_num = get_today_day(CHALLENGE_START)
        print(f"📅 Today is Day {day_num}")

    # Step 3: Find matching issue
    issue_title_pattern = f"Day {day_num}:"
    issues = repo.get_issues(state="open")

    issue = None
    for i in issues:
        if i.title.startswith(issue_title_pattern):
            issue = i
            break

    if not issue:
        print(f"⚠️ No open issue found for Day {day_num}")
        return

    print(f"✅ Found issue: {issue.title} (#{issue.number})")

    # Step 4: Create branch name
    # Remove the "Day {day_num}:" prefix from issue title before sanitizing
    title_without_day = issue.title[len(issue_title_pattern):].strip()

    safe_title = re.sub(r"[^a-zA-Z0-9]+", "-", title_without_day.lower()).strip("-")
    branch_name = f"day-{day_num}-{safe_title[:30]}"  # limit length

    # Step 5: Git checkout new branch
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"🌱 Created and switched to branch: {branch_name}")
    except subprocess.CalledProcessError:
        print(f"⚠️ Branch {branch_name} may already exist")

    # Step 6: Generate commit template
    commit_message = f"""{issue.title}

Related to issue #{issue.number}
Closes #{issue.number}
"""
    with open("COMMIT_TEMPLATE.txt", "w", encoding="utf-8") as f:
        f.write(commit_message)

    print("📝 Commit template saved to COMMIT_TEMPLATE.txt")

if __name__ == "__main__":
    main()
