#!/bin/bash

# This script use docker to decompress the bookmarks.jsonlz4 into bookmarks.json

# Current directory
currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the Mozilla profile folder from the file profiles.ini
firefoxProfileFolder=`crudini --get "$HOME/.mozilla/firefox/profiles.ini" Profile0 Path`

# Mozilla Firefox bookmarks backup folder
firefoxBackupFolder="$HOME/.mozilla/firefox/$firefoxProfileFolder/bookmarkbackups"

# Set the last backup
lastUpdatedFile=`ls -t "$firefoxBackupFolder" | head -n1`

# Set the output folder
outputFolder="$currentDir/output"

# Create the output folder if not exists
mkdir -p "output"

docker container run --rm -it -u $(id -u ${USER}):$(id -g ${USER}) --name MozLz4-decompress -v "$PWD":/usr/src/myapp -v "$PWD/.local":"/.local" -v "$firefoxBackupFolder":/usr/src/bookmarksFolder -w /usr/src/myapp -e PYTHONDONTWRITEBYTECODE=1 python:3.10-slim /bin/bash -l -c "pip install --no-cache-dir lz4 && python /usr/src/myapp/mozLz4-decompress/mozlz4.py -d /usr/src/bookmarksFolder/$lastUpdatedFile /usr/src/myapp/output/bookmarks.json"
docker container run --rm -it -u $(id -u ${USER}):$(id -g ${USER}) --name exportToMarkdown  -v "$PWD":/usr/src/myapp -v "$PWD/.local":"/.local" -v "$firefoxBackupFolder":/usr/src/bookmarksFolder -w /usr/src/myapp -e PYTHONDONTWRITEBYTECODE=1 python:3.10-slim /bin/bash -l -c "python3 exportToMarkdown.py /usr/src/myapp/output/bookmarks.json" > "$outputFolder/bookmarks.md"
