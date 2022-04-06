#! /usr/bin/env python3
"""Verify that an MBOX file contains all the messages in another MBOX file.

Each missing message has its id prenited to stdout and the message is
saved to missing.mbox. Ignores the parameter X-GM-THRID.

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
    if not str(message1).strip() == str(message2).strip():
        # Check complete messages content if the id matches. Save
        # message if there are inconsistencies.
        missing.append(message1)

if missing:
    print(f"Messages not in second mbox:")
    box_missing = mailbox.mbox("missing.mbox")
    for message in missing:
        print(message["Message-ID"])
        box_missing.add(message)
    box_missing.close()
