import asyncio
from datetime import datetime, timedelta
from csv import DictWriter
from os import getenv
from sys import exit

import aiohttp
from dotenv import load_dotenv


load_dotenv()

# === Config ===

JIRA_URL = getenv("JIRA_URL", "")
API_TOKEN = getenv("API_TOKEN", "")
EMAIL = getenv("EMAIL", "")
MAX_WORKERS = int(getenv("MAX_WORKERS", 11))  # Amount of concurrent tasks

if not JIRA_URL or not API_TOKEN or not EMAIL:
    print("Please set JIRA_URL, API_TOKEN, and EMAIL in the environment variables or .env file")
    exit(1)

AUTH_HEADER = aiohttp.BasicAuth(EMAIL, API_TOKEN)

spinner = ["|", "/", "-", "\\"]
results = []  # List to store results to CSV


def get_date_30_days_ago():
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


async def get_my_account_id(session):
    url = f"{JIRA_URL}/rest/api/3/myself"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data["accountId"]
        else:
            print("Unable to get accountId:", response.status, await response.text())
            exit(1)


async def fetch_issues(session):
    start_at = 0
    max_results = 100
    total = 1
    all_issues = []

    print(f"Searching for tasks updated after {get_date_30_days_ago()}...\n")

    while start_at < total:
        jql = f'updated >= "{get_date_30_days_ago()}"'
        url = f"{JIRA_URL}/rest/api/2/search"
        params = {"jql": jql, "fields": "summary,key", "maxResults": max_results, "startAt": start_at}

        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                issues = data["issues"]
                total = data["total"]
                print(f"Obtained {len(issues)} tasks (total: {total}), startAt: {start_at}")
                all_issues.extend(issues)
                start_at += max_results
            else:
                print(f"\nError fetching tasks: {response.status}, {await response.text()}")
                break

    return all_issues


async def analyze_issue(issue, session, my_account_id, semaphore, idx, total, progress_queue):  # noqa
    issue_key = issue["key"]
    issue_summary = issue["fields"]["summary"]
    created_by_me = False
    status_changed_by_me = False
    comment_by_me = False

    # Change history
    history_url = f"{JIRA_URL}/rest/api/2/issue/{issue_key}/changelog"
    async with session.get(history_url) as response:
        if response.status == 200:
            history_data = await response.json()
            for history in history_data["values"]:
                author = history.get("author", {})
                author_id = author.get("accountId", "")
                for item in history["items"]:
                    if item["field"] == "status" and author_id == my_account_id:
                        status_changed_by_me = True
                    if item["field"] == "reporter" and author_id == my_account_id:
                        created_by_me = True
        else:
            print(f"\nError while fetching task history {issue_key}: {response.status}")
            return

    # Comments
    comments_url = f"{JIRA_URL}/rest/api/2/issue/{issue_key}/comment"
    async with session.get(comments_url) as response:
        if response.status == 200:
            comments_data = await response.json()
            for comment in comments_data["comments"]:
                author = comment.get("author", {})
                if author.get("accountId", "") == my_account_id:
                    comment_by_me = True
        else:
            print(f"\nError while fetching task comments {issue_key}: {response.status}")
            return

    # Printing results
    if created_by_me or status_changed_by_me or comment_by_me:
        print(f"\ntask: {issue_key} - {issue_summary}")
        if created_by_me:
            print(" CREATED ")
        if status_changed_by_me:
            print(" MODIFIED ")
        if comment_by_me:
            print(" COMMENTED ")

        results.append(
            {
                "key": issue_key,
                "summary": issue_summary,
                "url": f"{JIRA_URL}/browse/{issue_key}",
                "created": str(created_by_me),
                "modified": str(status_changed_by_me),
                "commented": str(comment_by_me),
            }
        )

    await progress_queue.put(1)  # signal task completion


async def progress_monitor(total, progress_queue):
    processed = 0
    while processed < total:
        symbol = spinner[processed % len(spinner)]
        print(f"\r{symbol} Processing tasks: {processed}/{total}...", end="", flush=True)
        processed += await progress_queue.get()

    print("\nAll tasks processed!")


async def main():
    connector = aiohttp.TCPConnector(limit_per_host=MAX_WORKERS)
    async with aiohttp.ClientSession(auth=AUTH_HEADER, connector=connector) as session:
        my_account_id = await get_my_account_id(session)
        issues = await fetch_issues(session)
        total = len(issues)
        semaphore = asyncio.Semaphore(MAX_WORKERS)

        # Queue for tracking progress
        progress_queue = asyncio.Queue()

        # Start tasks
        tasks = [
            analyze_issue(issue, session, my_account_id, semaphore, idx, total, progress_queue)
            for idx, issue in enumerate(issues, start=1)
        ]
        tasks.append(progress_monitor(total, progress_queue))

        await asyncio.gather(*tasks)

    # CSV-saving
    with open("jira_activity_report0.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["key", "summary", "url", "created", "modified", "commented"]
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\nDone. Processed tasks: {total}")
    print("Results saved to CSV file: jira_activity_report0.csv")


if __name__ == "__main__":
    asyncio.run(main())
