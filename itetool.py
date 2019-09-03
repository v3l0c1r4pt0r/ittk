#!/usr/bin/env python3
# Tool for handling of ITEPKG firmware file
import argparse
import itepkg.itepkg
import os
import sys
from enum import Enum

class Action(Enum):
    FAIL = 0
    LIST = 1
    UNPACK = 2

def do_fail(pkg):
    print('No action was selected, leaving', file=sys.stderr)
    sys.exit(1)

def do_list(pkg):
    raise Exception('Not implemented')

def do_unpack(pkg):
    raise Exception('Not implemented')

action_handlers = {Action.FAIL: do_fail, Action.LIST: do_list, Action.UNPACK: do_unpack}

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="ITEPKG file to work on")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", help="List container elements", action="store_true")
    group.add_argument("-u", "--unpack",
            help="Unpack element of ID to directory (default=-1=all)",
            default=-1, metavar="ID", nargs='?')

    parser.add_argument("-d", "--directory", help="Unpack to DIR, instead CWD",
            type=str, metavar="DIR")

    args = parser.parse_args()
    print(args)
    action = Action.FAIL
    if args.list == True:
        action = Action.LIST
    elif args.unpack != -1:
        action = Action.UNPACK
        # if unpack given, default to -1
        if args.unpack == None:
            args.unpack = -1

    # open input file and read it
    fp = os.open(args.file, os.O_RDONLY)
    fsize = os.lseek(fp, 0, os.SEEK_END)
    os.lseek(fp, 0, os.SEEK_SET)
    b = os.read(fp, fsize)

    # parse ITEPKG
    pkg, b = itepkg.itepkg.ITEPKG.from_bytes(b)
    if (len(b) > 0):
        print("Superfluous bytes after ITEPKG. Make sure you gave proper ITEPKG file", file=sys.stderr)

    print(' ITEPKG', end='')
    for e in pkg.entries:
        print('')
        if isinstance(e, itepkg.entries.MemoryEntry):
            print(' |- SMEDIA(',hex(e.address.integer),')', end='')
        elif isinstance(e, itepkg.entries.DirectoryEntry):
            print(' |- Dir(',e.filename.array[0].decode('utf-8'),')', end='')
        elif isinstance(e, itepkg.entries.FileEntry):
            print(' |- File(',e.filename.array[0].decode('utf-8'),')', end='')
        elif isinstance(e, itepkg.entries.UnknownEntry):
            print(' |- Unknown(',hex(e.unknown1.integer),hex(e.unknown2.integer),')', end='')
        elif isinstance(e, itepkg.entries.EndEntry):
            print(' |- End', end='')
        else:
            print(' |-', type(e), end='')
    print('\r `- ')

    # TODO: do stuff

    # cleanup
    os.close(fp)

if __name__ == '__main__':
    main(sys.argv)
