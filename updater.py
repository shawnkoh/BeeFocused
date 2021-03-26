"""Script that integrates Focus with Beeminder."""
import os

from enum import Enum
from typing import NamedTuple

import beeminder
import notifier

from dotenv import load_dotenv

# CONFIG

load_dotenv()
beeminder.username = os.getenv("USERNAME")
# Retrieved from https://www.beeminder.com/api/v1/auth_token.json
beeminder.auth_token = os.getenv("AUTH_TOKEN")
# The location of where your log file should be.
LOG_DIRECTORY = os.path.expanduser("~/repos/BeeFocused/log.txt")
# The Beeminder goal that you want to automatically update.
GOAL = "test"


class Action(Enum):
    """An Action describes the nature of an user event in Focus."""

    START = 0
    BREAK = 1
    UNBREAK = 2
    STOP = 3


class Event(NamedTuple):
    """An event is a Focus event that occured."""

    action: Action
    timestamp: int


events = []

# Reformat the log because the order produced by the bash scripts are not
# deterministic because Focus does not always execute the custom events in order.

log_file = open(LOG_DIRECTORY)

for line in log_file:
    params = line.split(": ")
    action = Action[params[0].upper()]
    timestamp = int(params[1])
    event = Event(action, timestamp)
    events.append(event)

log_file.close()

# Remove duplicate events
events = set(events)

# Sort by timestamp then action
events = sorted(events, key=lambda event: (event.timestamp, event.action.value))

start_timestamp = 0
stop_timestamp = 0

break_start_timestamp = 0
break_duration = 0


def _started():
    return start_timestamp != 0


def _on_break():
    return break_start_timestamp != 0


def _work_duration():
    return stop_timestamp - start_timestamp - break_duration


for event in events:
    if not _started():
        if event.action == Action.START:
            start_timestamp = event.timestamp
        continue

    if event.action == Action.STOP:
        stop_timestamp = event.timestamp
        break

    if event.action == Action.BREAK:
        break_start_timestamp = event.timestamp
        continue

    if _on_break() and event.action == Action.UNBREAK:
        break_duration += event.timestamp - break_start_timestamp
        break_start_timestamp = 0
        continue

if not _started():
    quit()

duration = _work_duration()

minutes, seconds = divmod(duration, 60)
hours, minutes = divmod(minutes, 60)

value = duration / 60 / 60

beeminder.create_datapoint(GOAL, value, "Auto-entered via BeeFocused")

notifier.notify(
    "BeeFocused", f"Focused for {hours}h {minutes}m {seconds}s. Uploaded to Beeminder."
)
