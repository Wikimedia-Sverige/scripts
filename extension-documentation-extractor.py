#! /usr/bin/env python3


import json
import sys
from collections import OrderedDict
import argparse
import subprocess
import re


RE_HOOK_FUNCTION = re.compile(r"^\tpublic static function on([^\(]+)\(")


def print_extension_json_info(extension_json_file):
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
    log = subprocess.run(
        ["git", "-C", extension_path, "log", "--date=short"],
        stdout=subprocess.PIPE,
        universal_newlines=True
    ).stdout
    date = log.split("\n")[2].split("   ")[1]
    return date


def print_hooks():
    i = 1
    with open("{}/WikispeechHooks.php".format(extension_path)) as f:
        for line in f:
            match = RE_HOOK_FUNCTION.match(line)
            if match:
                print("|hook{} = {}".format(i, match.group(1)))
                i += 1


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
