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
echo "stop: "$(date +%s)"" >> ~/repos/BeeFocused/log.txt
python3 ~/repos/BeeFocused/script.py
```

Run this script when Focus **breaks**
```
echo "break: "$(date +%s)"" >> ~/repos/BeeFocused/log.txt
```

Run this script when Focus **unbreaks**
```
echo "unbreak: "$(date +%s)"" >> ~/repos/BeeFocused/log.txt
```

5. Update the directories in #4 to where you installed it.

6. Update the directory in script.py to where you installed it.

7. Run ```poetry install```

## VSCode Integration

If you're using VSCode, you need to run ```poetry config virtualenvs.in-project true``` in your shell.
Afterwards, change your environment to the poetry instance.