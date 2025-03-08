import os
import sys
import time

# TODO: Add logger (with logging)

from collections.abc import Callable
from typing import Dict

from recurrent_tasks import main_recurrent_tasks

NOTION_SECRET = "NOTION_SEC"

SCRIPTS_DICT: Dict[str, Callable[[str], None]] = {
    "recurrent_tasks": main_recurrent_tasks,
}


def callScript(script_key: str):
    try:
        notion_api_key = os.environ[NOTION_SECRET]
    except Exception:
        raise Exception(f"error getting notion secret with env var name '{NOTION_SECRET}'")
    SCRIPTS_DICT[script_key](notion_api_key)


def validation_or_exit_err(predicate: Callable[[], bool], err_msg: str):
    if not predicate():
        print(f"Finish with error: {err_msg}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting...")
    validation_or_exit_err(lambda: len(sys.argv) >= 2, "missing input enum script to execute")
    script_to_execute = sys.argv[1].lower()
    validation_or_exit_err(lambda: script_to_execute in SCRIPTS_DICT, "script key not found")

    print(f"Script to execute: {script_to_execute}")
    start_time = time.time()
    err_found = False
    try:
        callScript(script_to_execute)
        print("Finish ok")
    except Exception as ex:
        print(f"Finish with error: {ex}")
        err_found = True

    execution_time_sec = time.time() - start_time
    execution_time_ms = execution_time_sec * 1000
    print(f"Execution time: {execution_time_sec:.2f} sec | {execution_time_ms:.2f} ms")
    exit_code = 1 if err_found else 0
    sys.exit(exit_code)
