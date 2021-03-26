# BeeFocused

BeeFocused is a script that integrates [Focus](https://heyfocus.com/) with [Beeminder](https://www.beeminder.com/).

It automatically sends the time you spent focused (excluding breaks) to Beeminder.

# Installation Instructions

1. Clone this repository

2. Install [python](https://www.python.org/downloads/)

3. Install [poetry](https://github.com/python-poetry/poetry)

4. Open Focus Preferences > Scripting and paste the following

Run this script when Focus **starts**
```
echo "start: "$(date +%s)"" > ~/repos/BeeFocused/log.txt
```

Run this script when Focus **stops**
```
export PATH=$PATH:~/.poetry/bin
cd ~/repos/BeeFocused
echo "stop: "$(date +%s)"" >> log.txt
poetry run python updater.py
```

Run this script when Focus **breaks**
```
echo "break: "$(date +%s)"" >> ~/repos/BeeFocused/log.txt
```

Run this script when Focus **unbreaks**
```
echo "unbreak: "$(date +%s)"" >> ~/repos/BeeFocused/log.txt
```

5. Update the directories in #4 to where you installed this.

6. Update the LOG_DIRECTORY in updater.py to where you want your log file to be at.

7. Retrieve your auth token from https://www.beeminder.com/api/v1/auth_token.json

8. Create a .env file in this folder with the following
```
USERNAME=<Your Beeminder username>
AUTH_TOKEN=<Your auth token>
```

9. Open your terminal app and run ```poetry install --no-dev```
# Developer Instructions

## VSCode Integration

If you are using VSCode, you need to run ```poetry install``` again to install development dependencies, and ```poetry config virtualenvs.in-project true``` in your shell.
Afterwards, change your environment to the poetry instance.
