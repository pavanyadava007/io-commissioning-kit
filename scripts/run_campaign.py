"""Run the seeded fault-injection campaign (same as `iokit campaign`)."""

import sys

from iokit.cli import main

if __name__ == "__main__":
    sys.exit(main(["campaign", *sys.argv[1:]]))
