import subprocess
import os

from enum import Enum
from typing import NamedTuple
from operator import itemgetter

# CHANGE TO YOUR DIRECTORY
LOG_DIRECTORY = os.path.expanduser("~/repos/BeeFocused/log.txt")

# Helper to display a notification on MacOS via AppleScript.
# Credit: https://stackoverflow.com/questions/17651017/python-post-osx-notification
CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

def notify(title, text):
  subprocess.call(['osascript', '-e', CMD, title, text])

# The log order produced by the bash scripts are not deterministic because Focus does not always execute the custom events in order.
class Action(Enum):
    START = 0
    BREAK = 1
    UNBREAK = 2
    STOP = 3

class Event(NamedTuple):
    action: Action
    timestamp: int

events = []

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
events = sorted(events, key = lambda event: (event.timestamp, event.action.value))

start_timestamp = 0
stop_timestamp = 0

break_start_timestamp = 0
break_duration = 0

def started():
    return start_timestamp != 0

def on_break():
    return break_start_timestamp != 0

def work_duration():
    return stop_timestamp - start_timestamp - break_duration

for event in events:
    if not started():
        if event.action == Action.START:
            start_timestamp = event.timestamp
        continue

    if event.action == Action.STOP:
        stop_timestamp = event.timestamp
        break

    if event.action == Action.BREAK:
        break_start_timestamp = event.timestamp
        continue

    if on_break() and event.action == Action.UNBREAK:
        break_duration += (event.timestamp - break_start_timestamp)
        break_start_timestamp = 0
        continue

if not started():
    quit()

# POST to Beeminder's API

notify("BeeFocused", f"Uploaded to Beeminder {work_duration()}")