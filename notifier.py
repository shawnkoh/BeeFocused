import subprocess

# Helper to display a notification on MacOS via AppleScript.
# Credit: https://stackoverflow.com/questions/17651017/python-post-osx-notification
_CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

def notify(title, text):
  subprocess.call(['osascript', '-e', _CMD, title, text])