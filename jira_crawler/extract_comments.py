from datetime import datetime, timedelta
from os import getenv
from sys import exit

from dotenv import load_dotenv
from requests import get
from requests.auth import HTTPBasicAuth


load_dotenv()


# Set up the JIRA URL and authentication
jira_url = getenv("JIRA_URL", "")
api_token = getenv("API_TOKEN", "")
email = getenv("EMAIL", "")

if not jira_url or not api_token or not email:
    print("Please set JIRA_URL, API_TOKEN, and EMAIL in the environment variables or .env file")
    exit(1)

# Set up the API token and email
auth = HTTPBasicAuth(email, api_token)

spinner = ["|", "/", "-", "\\"]


def get_date_30_days_ago():
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


# Obtaining all modified tasks for the last month
def get_my_account_id():
    url = f"{jira_url}/rest/api/3/myself"
    response = get(url, headers={"Content-Type": "application/json"}, auth=auth)
    if response.status_code == 200:
        return response.json()["accountId"]
    else:
        print("Unable to get accountId:", response.status_code, response.text)
        exit(1)


# Get all modified tasks for the last month
def get_issues_updated_last_30_days(my_account_id):
    start_at = 0
    max_results = 100
    total = 1

    print(f"Finding tasks updated after {get_date_30_days_ago()}...\n")

    while start_at < total:
        jql = f'updated >= "{get_date_30_days_ago()}"'
        url = f"{jira_url}/rest/api/2/search"
        params = {"jql": jql, "fields": "summary,key", "maxResults": max_results, "startAt": start_at}

        response = get(url, headers={"Content-Type": "application/json"}, auth=auth, params=params)

        if response.status_code == 200:
            data = response.json()
            issues = data["issues"]
            total = data["total"]

            print(f"Obtained {len(issues)} tasks (total: {total}), startAt: {start_at}")

            for idx, issue in enumerate(issues, start=start_at + 1):
                symbol = spinner[idx % len(spinner)]
                print(f"\r{symbol} Processing task {idx}/{total}: {issue['key']}", end="", flush=True)
                analyze_issue(issue["key"], issue["fields"]["summary"], my_account_id)

            start_at += max_results
        else:
            print(f"\nError while requesting tasks: {response.status_code}, {response.text}")
            break

    print(f"\nDone. Total tasks processed: {start_at}")


# Analyze the task
def analyze_issue(issue_key, issue_summary, my_account_id):
    created_by_me = False
    status_changed_by_me = False
    comment_by_me = False

    # Change history
    history_url = f"{jira_url}/rest/api/2/issue/{issue_key}/changelog"
    history_response = get(history_url, headers={"Content-Type": "application/json"}, auth=auth)

    if history_response.status_code == 200:
        history_data = history_response.json()
        for history in history_data["values"]:
            author = history.get("author", {})
            author_id = author.get("accountId", "")
            for item in history["items"]:
                if item["field"] == "status" and author_id == my_account_id:
                    status_changed_by_me = True
                if item["field"] == "reporter" and author_id == my_account_id:
                    created_by_me = True
    else:
        print(f"\nError while obtaining task history {issue_key}: {history_response.status_code}")
        return

    # Comments
    comments_url = f"{jira_url}/rest/api/2/issue/{issue_key}/comment"
    comments_response = get(comments_url, headers={"Content-Type": "application/json"}, auth=auth)

    if comments_response.status_code == 200:
        comments_data = comments_response.json()
        for comment in comments_data["comments"]:
            author = comment.get("author", {})
            if author.get("accountId", "") == my_account_id:
                comment_by_me = True
    else:
        print(f"\nError while obtaining comments for task {issue_key}: {comments_response.status_code}")
        return

    # Print if there were actions
    if created_by_me or status_changed_by_me or comment_by_me:
        print(f"\ntask: {issue_key} - {issue_summary}")
        if created_by_me:
            print(" Created ")
        if status_changed_by_me:
            print("  Modified ")
        if comment_by_me:
            print("  Commented ")


# Run
if __name__ == "__main__":
    account_id = get_my_account_id()
    get_issues_updated_last_30_days(account_id)
