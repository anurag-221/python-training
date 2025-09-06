
from github import Github
import json
import csv
import re
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

# =============== STEP 1: Import or Update Labels from JSON ===============
print("\n📌 Importing / Updating Labels...")

# Load labels JSON
with open("labels_100days.json") as f:
    labels = json.load(f)


# Fetch existing labels from GitHub
existing_labels = {label.name: label for label in repo.get_labels()}

for label in labels:
    name = label["name"]
    color = label["color"]
    description = label.get("description", "")

    if name in existing_labels:
        gh_label = existing_labels[name]

        # Check if update is needed
        needs_update = (gh_label.color.lower() != color.lower()) or (gh_label.description != description)

        if needs_update:
            try:
                gh_label.edit(name=name, color=color, description=description)
                print(f"🔄 Updated label: {name}")
            except Exception as e:
                print(f"⚠️ Error updating {name}: {e}")
        else:
            print(f"⏩ Skipped (already correct): {name}")
    else:
        try:
            repo.create_label(name=name, color=color, description=description)
            print(f"✅ Created label: {name}")
        except Exception as e:
            print(f"⚠️ Error creating {name}: {e}")


label_names = [label["name"] for label in labels]

# =============== Helper: Find Phase Label ===============
def get_phase_label(day_num: int) -> str:
    """Return Phase label based on day number."""
    if 1 <= day_num <= 25:
        return "Phase-1"
    elif 26 <= day_num <= 50:
        return "Phase-2"
    elif 51 <= day_num <= 75:
        return "Phase-3"
    elif 76 <= day_num <= 100:
        return "Phase-4"
    return None

# =============== STEP 2: Create or Update Issues from CSV ===============
print("\n📌 Creating / Updating Issues from CSV...")

# Fetch existing issues (open + closed)
existing_issues = {issue.title: issue for issue in repo.get_issues(state="all")}

with open("python_ai_datascience_100days.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not row:
            continue  # skip empty lines

        day = row[0].strip()       # e.g., "Day 1"
        task = row[1].strip()      # e.g., "Install Python, Git..."
        description = row[2].strip() if len(row) > 2 else ""
        file_ref = row[3].strip() if len(row) > 3 else ""

        # Normalize day → match label (replace space with dash)
        normalized_day = day.replace(" ", "-")  # "Day 1" → "Day-1"

        # Extract number from "Day 1"
        match = re.search(r"(\d+)", day)
        day_num = int(match.group(1)) if match else None

        # Find Phase label
        phase_label = get_phase_label(day_num) if day_num else None

        issue_title = f"{day}: {task}"
        issue_body = f"""### Task Details  
**Day:** {day}  
**Task:** {task}  

**Description:**  
{description}  

**File Reference:** {file_ref}  
"""

        # Attach labels if exist
        issue_labels = []
        if normalized_day in label_names:
            issue_labels.append(normalized_day)
        if phase_label and phase_label in label_names:
            issue_labels.append(phase_label)

        if issue_title in existing_issues:
            gh_issue = existing_issues[issue_title]

            # Check if update is needed
            labels_need_update = sorted([l.name for l in gh_issue.labels]) != sorted(issue_labels)
            body_needs_update = gh_issue.body.strip() != issue_body.strip()

            if labels_need_update or body_needs_update:
                try:
                    gh_issue.edit(body=issue_body, labels=issue_labels)
                    print(f"🔄 Updated issue: {issue_title}")
                except Exception as e:
                    print(f"⚠️ Error updating {issue_title}: {e}")
            else:
                print(f"⏩ Skipped (already correct): {issue_title}")
        else:
            try:
                repo.create_issue(
                    title=issue_title,
                    body=issue_body,
                    labels=issue_labels
                )
                print(f"✅ Created issue: {issue_title} with labels {issue_labels}")
            except Exception as e:
                print(f"⚠️ Error creating {issue_title}: {e}")

