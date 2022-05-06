#! /usr/bin/env python3
"""Verify all messages in MBOX file (`mbox1`) are in other MBOX file (`mbox2`)

Each missing message has its id printed to stdout and the message is
saved to missing.mbox. Ignores the parameter X-GM-THRID.

Requirements:
* tqdm>=4.64.0,==4.*
"""

from argparse import ArgumentParser
import mailbox

from tqdm import tqdm


parser = ArgumentParser()
parser.add_argument("mbox1")
parser.add_argument("mbox2")
args = parser.parse_args()

box1 = mailbox.mbox(args.mbox1, create=False)
box2 = mailbox.mbox(args.mbox2, create=False)

messages2 = {m["Message-ID"]: m for m in box2}

missing = []

for message1 in tqdm(box1):
    # Remove extra parameter added by Groups.
    del message1["X-GM-THRID"]
    message2 = messages2.get(message1["Message-ID"])
    if message2 is None:
        # Save message if it's in the first mailbox, but not the
        # second.
        missing.append(message1)
        continue

    del message2["X-GM-THRID"]
    if str(message1).strip() != str(message2).strip():
        # Check complete messages content if the id matches. Save
        # message if there are inconsistencies.
        missing.append(message1)

if missing:
    print("Messages missing from or different in second mbox:")
    box_missing = mailbox.mbox("missing.mbox")
    for message in missing:
        print(message["Message-ID"])
        box_missing.add(message)
    box_missing.close()
    print("Messages written to missing.mbox.")
