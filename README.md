# firefox-bookmarks-to-markdown

Converts the FireFox bookmarks to Markdown. Filters are allowed in order to accept or deny the conversion of the specified categories.

## Prerequisites

Remember to checkout the git submodule ``mozLz4-decompress`` with:

```bash
git submodule update --init --recursive
```

You also need ``crudini`` for loading the location of the bookmark files, please install it with:

```bash
apt install crudini
```

And you need python3, check it is installed with:

```bash
python3 --version
```

## Usage

You can convert the FireFox bookmarks file (already converted from jsonlz4 to JSON) to Markdown with the following syntax:

```bash
python3 exportToMarkdown.py path/to/bookmarks.json > path/to/bookmarks.md [--allowed "cat1" "cat2" "cat3" ...] [--denied "cat4" "cat5" ...]
```

If the parameter ``--allowed`` is not used, all the bookmarks are converted to Markdown.

With the argument ``--allowed``, only the selected categories will be converted to Markdown. Pay attention that **you need to pass the category and all the parent categories**, otherwise the category will not be converted (because some parent will not be allowed).

With the argument ``--denied``, all the categories except the selected will be converted to Markdown.

Note: You can get the bash script ``script.sh`` to run the prerequisite steps and to convert the bookmarks to Markdown. If you want to run the python script in docker, create the folder ``.local`` and check the file ``docker-script.sh``.

### Usage example

E.g. Let's have the following bookmark structure:

- menu
  - Scienze
    - Math
      - link1
      - link2
      - link3

To convert the links, you nedd to pass all the parents as the following:

```bash
python3 exportToMarkdown.py bookmarks.json --allowed '' 'menu' 'Scienze' 'Math'
```

To skip the conversion of links, you can select the parent category, as the following:

```bash
python3 exportToMarkdown.py bookmarks.json  --denied 'Math'
```

## Customization

The script ``script.sh`` allow you to convert the bookmarks file to a Markdown file.

The first step of this script is the location of the bookmark files, referenced as ``$FF_PROFILE_ID``. The path is saved in the Firefox profile, which is saved in ``$HOME/.mozilla/firefox/profiles.ini``. The ``crudini`` tool let the reading of this file.

Once located the FireFox bookmark file, saved in the file ``$HOME/.mozilla/firefox/$FF_PROFILE_ID.default[-esr]/bookmarkbackups/bookmarks-xyz...abc.jsonlz4``, the python module [mozLz4-decompress](https://github.com/codingepaduli/mozLz4-decompress#mozlz4-decompress) is used to convert it from jsonlz4 to JSON;

Last step, the script will convert the JSON file in Markdown, running the python module ``exportToMarkdown.py``.

## License

MIT License. Read the file LICENSE
