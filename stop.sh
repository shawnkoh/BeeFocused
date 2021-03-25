echo "stop: "$(date +%s)"" >> log.txt
# Was unable to execute the poetry binary in Focus's custom scripts so manually call it here instead.
~/.poetry/bin/poetry run python ~/repos/BeeFocused/updater.py