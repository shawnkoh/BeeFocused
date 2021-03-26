# Focus executes a custom shell script. Couldn't load poetry into PATH by sourcing profiles so manually add it here instead
export PATH=$PATH:~/.poetry/bin

# Poetry looks for the pyproject.toml in the current working directory.
# CHANGEME
cd ~/repos/BeeFocused

echo "stop: "$(date +%s)"" >> log.txt

poetry run python updater.py