# notion-automations
Notion automations repo

- [Automation of recurrent tasks](recurrent_tasks.py)

## Requirements

- Python 3.x

## Available scripts keys:

- [Recurrent_tasks](recurrent_tasks.py):
  1. Get all current recurrent tasks database.
  2. Get all current tasks with "wait" checked.
  3. Filter recurrent tasks that are not "Done" checked in the tasks database with "wait" checked.
  4. Calculates the next due date with recurrent next days field from now
  5. Create task in tasks database with "Wait" check if not exist in curren tasks with same title. 
- ...

## Execution

- Requires env var `NOTION_SEC` with Notion API_KEY set.

1. Go to root repository and execute:

    ```bash
    pip install -r requirements.txt
    ```

2. Then execute:

    ```bash
    py ./main.py <script_key> 
    ```

    For example:
    ```bash
    py ./main.py recurrent_tasks
    ```