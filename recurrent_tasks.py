import requests
from datetime import date, datetime, timedelta, time

# TODO: DO REFACTORS!!!

RECURRING_DB_ID = "1aa9514d723c80c3b9abda16a74ec3b3"
TASKS_DB_ID = "16b9514d723c80d6b81ac1d9d8496218"


def is_success_response(name: str, response, ex=None) -> bool:
    if not response.ok:
        print(f"Error {name} response with status_code {response.status_code}")
        raise ex
    else:
        print(f"Success {name} response")
    return response.ok


def get_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def get_recurrent_tasks(headers):
    url = f"https://api.notion.com/v1/databases/{RECURRING_DB_ID}/query"
    res = requests.post(url, headers=headers)
    if not res.ok:
        raise Exception(
            f"Error get_recurrent_tasks with status_code {res.status_code} and content {res.content}")
    return res.json().get("results", [])


def get_reminders(headers):
    # TODO: Add filters in query params to optimize memory filter
    url = f"https://api.notion.com/v1/databases/{TASKS_DB_ID}/query"
    res = requests.post(url, headers=headers)
    if not res.ok:
        raise Exception(
            f"Error get_reminders tasks with status_code {res.status_code} and content {res.content}")
    return res.json().get("results", [])


def create_reminder(headers, name, alert_date):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": TASKS_DB_ID},
        "properties": {
            "Siguiente acción": {"title": [{"text": {"content": name}}]},
            "Día alerta": {"date": {"start": alert_date.isoformat()}},
            "⏳ ": {"type": "checkbox", "checkbox": True}
        }
    }
    print(f"creating reminder because it doesn't exist with data={data}")
    res = requests.post(url, headers=headers, json=data)
    if not res.ok:
        raise Exception(
            f"Error create_reminder task with name {name}, status_code {res.status_code} and content {res.content}")

    print(f"Success creating reminder {name}")
    return res.json()


def already_exist_reminder(reminders, name):
    return any(
        r["properties"]["Siguiente acción"]["title"][0]["text"]["content"].strip() == name
        for r in reminders
    )


def main_recurrent_tasks(notion_api_key: str):
    headers = get_headers(notion_api_key)
    recurrent_tasks = get_recurrent_tasks(headers)
    existing_reminders = get_reminders(headers)

    existing_reminders = list(
        filter(lambda r: (not r["properties"]["Hecho?"]["checkbox"]) and r["properties"]["⏳ "]["checkbox"],
               existing_reminders))

    today = date.today()

    for task in recurrent_tasks:
        name = task["properties"]["Name"]["title"][0]["text"]["content"].strip()
        days = task["properties"]["Dias de recurrencia"]["number"]
        status = task["properties"]["Estado"]["select"]["name"]
        if status != "Activo":
            continue
        alert_date = today + timedelta(days=days)
        alert_date = datetime.combine(alert_date, time(13, 0, 0))
        # Check if reminder already exists
        if not already_exist_reminder(existing_reminders, name):
            create_reminder(headers, name, alert_date)
