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


RE_HOOK_FUNCTION = re.compile(r"^\tpublic static function on([^\(]+)\(")


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
!Option
!Default value
!Documentation"""
    print(headers_string)
    parameters = []
    for key, value in config.items():
        row = """|-
| {option}
| <source lang="json">{default}</source>
| DOCUMENTATION GOES HERE"""\
        .format(option=key, default=json.dumps(value, indent=4))
        print(row)
        parameters.append("* $wg{}".format(key))
    print("|}")
    print()

    print("===Infobox===")
    print("|version = {}".format(extension_dict["version"]))
    print()
    print("|update = {}".format(get_update_date()))
    print()
    print("|parameters = \n{}".format("\n".join(parameters)))
    print()
    print_hooks()


def get_update_date():
    """Get the date for the last commit from ``git log``.

    """
    log = subprocess.run(
        ["git", "-C", extension_path, "log", "--date=short"],
        stdout=subprocess.PIPE,
        universal_newlines=True
    ).stdout
    date = log.split("\n")[2].split("   ")[1]
    return date


def print_hooks():
    """Print out the hooks used by the extension.

    """
    i = 1
    with open("{}/WikispeechHooks.php".format(extension_path)) as f:
        for line in f:
            match = RE_HOOK_FUNCTION.match(line)
            if match:
                print("|hook{} = {}".format(i, match.group(1)))
                i += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Extension directory must be supplied.")
        sys.exit(1)
    extension_path = sys.argv[1]
    extension_json_path = "{}/extension.json".format(extension_path)
    try:
        extension_json_file = open(extension_json_path)
    except:
        print("Failed to open file: {}".format(extension_json_path))
        sys.exit(1)
    print_extension_json_info(extension_json_file)
