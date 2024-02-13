#!/bin/bash

# This script decompress the bookmarks.jsonl4 into bookmarks.json

# Current directory
currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the Mozilla profile folder from the file profiles.ini
firefoxProfileFolder=$(crudini --get "$HOME/.mozilla/firefox/profiles.ini" Profile0 Path)

# Mozilla Firefox bookmarks backup folder
firefoxBackupFolder="$HOME/.mozilla/firefox/$firefoxProfileFolder/bookmarkbackups"

# Set the last backup
lastUpdatedFile=$(ls -t "$firefoxBackupFolder" | head -n1)

# Set the output folder
outputFolder="$currentDir/output"

# Create the output folder if not exists
mkdir -p "$outputFolder"

# decompress the bookmarks.json
python3 "$currentDir/mozLz4-decompress/mozlz4.py" -d "$firefoxBackupFolder/$lastUpdatedFile" "$outputFolder/bookmarks.json"

# Debugging (optional step): pretty print the json file
python3 -m json.tool "$outputFolder/bookmarks.json" > "$outputFolder/bookmarksFormatted.json"

# Debugging (optional step): Convert the bookmarks.json in bookmarks.md (pretty print in Markdown)
python3 "$currentDir/exportToMarkdown.py" "$outputFolder/bookmarks.json" > "$outputFolder/bookmarks.md"

#### Start coping from here

