
import os
import json
import urllib.request

KEYWORDS = {
    "Bug": ["bug", "error", "crash", "exception"],
    "API Issue": ["api", "endpoint", "404", "500"],
    "Frontend Issue": ["frontend", "ui", "button", "dashboard"],
    "Performance": ["slow", "latency", "timeout"],
    "Authentication": ["login", "authentication", "token"],
    "Data Warehousing": [
        "data warehouse", "etl", "pipeline",
        "snowflake", "redshift", "bigquery"
    ]
}

event_path = os.environ["GITHUB_EVENT_PATH"]
token = os.environ["GITHUB_TOKEN"]
repository = os.environ["GITHUB_REPOSITORY"]

with open(event_path, encoding="utf-8") as file:
    event = json.load(file)

issue = event["issue"]
issue_number = issue["number"]
text = (
    issue.get("title", "") + " " +
    (issue.get("body") or "")
).lower()

labels = [
    label
    for label, keywords in KEYWORDS.items()
    if any(keyword in text for keyword in keywords)
]

if labels:
    url = (
        f"https://api.github.com/repos/"
        f"{repository}/issues/{issue_number}/labels"
    )

    data = json.dumps({"labels": labels}).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "issue-filter-bot"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        print("Labels assigned:", labels)
else:
    print("No matching keywords found.")
