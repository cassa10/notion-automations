import os

from recurrent_tasks import main_recurrent_tasks

NOTION_SECRET = "NOTION_SEC"


def callScript():
    notion_api_key = os.environ[NOTION_SECRET]
    main_recurrent_tasks(notion_api_key)
    print("Ok")


if __name__ == "__main__":
    print("Starting...")
    callScript()
    print("Finish ok")
