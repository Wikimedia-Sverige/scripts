#! /usr/bin/env python3
"""Extract information about a MediaWiki extension for the documentation page.

The output is in wikitext, making it possible to copy directly to the
documentation page. There are two blocks of information, one for the
configuration and one for the info box.

The configuration is output as a table with variable names and default
values taken from *extension.js*.

The info box information is output as lines with template
parameters. The following parameters are printed:

* ``version`` - from *extension.js*
* ``update`` - from ``git log``
* ``parameters`` - from the hooks php file

"""

import json
import sys
from collections import OrderedDict
import subprocess
import re
import argparse


RE_HOOK_FUNCTION = re.compile(r"^\tpublic static function on([^\(]+)\(")
RE_DATE = re.compile(r"^Date:\s+(\d{4}-\d{2}-\d{2}$)", re.MULTILINE)


def print_extension_json_info(extension_json_file):
    """Print out relevant information about the extension.

    Parameters
    ----------
    extension_json_file : file
        The extension.js file in the extension directory.

    """
    extension_dict = json.load(
        extension_json_file,
        object_pairs_hook=OrderedDict
    )
    print("=== Config ===")
    config = extension_dict["config"]
    headers_string = """{| class="wikitable"
|-
! Option
! Default value
! Documentation"""
    print(headers_string)
    parameters = []
    for key, value in config.items():
        documentation = "DOCUMENTATION GOES HERE"
        if args.manifest_version == 1:
            default = json.dumps(value, indent=4)
        elif args.manifest_version == 2:
            if "description" in value:
                documentation = value["description"]
                if type(documentation) == list:
                    documentation = "".join(documentation)
            default = json.dumps(value["value"], indent=4)
        row = """|-
| {option}
| <source lang="json">{default}</source>
| {documentation}"""\
        .format(
            option=key,
            default=default,
            documentation=documentation
        )
        print(row)
        parameters.append("* $wg{}".format(key))
    print("|}")
    print()

    print("===Infobox===")
    print("| version = {}".format(extension_dict["version"]))
    print()
    print("| update = {}".format(get_update_date()))
    print()
    print("| parameters = \n{}".format("\n".join(parameters)))
    print()
    print_hooks()


def get_update_date():
    """Get the date for the last commit from ``git log``.

    """
    log = subprocess.run(
        ["git", "-C", args.extension_path, "log", "--date=short"],
        stdout=subprocess.PIPE,
        universal_newlines=True
    ).stdout
    date = RE_DATE.search(log).group(1)
    return date


def print_hooks():
    """Print out the hooks used by the extension.

    """
    i = 1
    with open("{}/WikispeechHooks.php".format(args.extension_path)) as f:
        for line in f:
            match = RE_HOOK_FUNCTION.match(line)
            if match:
                print("| hook{} = {}".format(i, match.group(1)))
                i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extension-path", "-e", default=".")
    parser.add_argument("--manifest-version", "-m", default="2", type=int)
    args = parser.parse_args()
    extension_json_path = "{}/extension.json".format(args.extension_path)
    with open(extension_json_path) as extension_json_file:
        print_extension_json_info(extension_json_file)
