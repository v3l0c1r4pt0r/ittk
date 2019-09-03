#!/usr/bin/env python3
# Tool for handling of ITEPKG firmware file
import argparse
import itepkg.itepkg
import os
import sys
from enum import Enum
from itepkg.entries import Entry
import itepkg.entries

def generate_fname(dirname, i, entry):
    if isinstance(entry, itepkg.entries.MemoryEntry):
        return "{}/{}.smedia".format(dirname, i)
    elif isinstance(entry, itepkg.entries._FSEntry):
        return "{}/fs/{}".format(dirname, entry.filename.array[0][:-1].decode('utf-8'))
    else:
        return None

def get_data_object(entry):
    """Returns data object, if any, contained in entry object"""
    if isinstance(entry, itepkg.entries.MemoryEntry):
        return entry.content
    elif isinstance(entry, itepkg.entries.FileEntry):
        return bytes(entry.contents)[4:]
    else:
        return None

def write_file(fname, data):
    """Write bytes object to file"""
    fp = os.open(fname, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
    os.write(fp, data)
    os.close(fp)

def print_smedia(entry):
    """Prepare string for SMEDIA chunk of ITEPKG file"""
    return "SMEDIA({})".format(hex(entry.address.integer))

def print_dir(entry):
    """Prepare string for directory chunk of ITEPKG file"""
    return "Dir('{}')".format(entry.filename.array[0].decode('utf-8'))

def print_file(entry):
    """Prepare string for file chunk of ITEPKG file"""
    return "File('{}')".format(entry.filename.array[0].decode('utf-8'))

def print_unknown(entry):
    """Prepare string for unknown chunk of ITEPKG file"""
    return "Unknown({}, {})".format(hex(entry.unknown1.integer), hex(entry.unknown2.integer))

def print_end(entry):
    """Prepare string for end chunk of ITEPKG file"""
    return "End"

printers = {Entry.Memory: print_smedia, Entry.Directory: print_dir,
        Entry.File: print_file, Entry.Unknown: print_unknown,
        Entry.End: print_end}

class Action(Enum):
    FAIL = 0
    LIST = 1
    UNPACK = 2

def do_fail(pkg, args):
    print('No action was selected, leaving', file=sys.stderr)
    sys.exit(1)

def do_list(pkg, args):
    print(' ITEPKG', end='')
    for e in pkg.entries:
        print('')
        if hasattr(e, 'type'):
            print(' |- {}'.format(printers[e.type](e)), end='')
        else:
            print(' |-', type(e), end='')
    print('\r `- ')

def do_unpack(pkg, args):
    outdir = args.directory
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if os.path.isfile(outdir):
        raise Exception(
                "Path {} already exists and is not directory".format(outdir))

    for i, e in enumerate(pkg.entries):
        fname = generate_fname(outdir, i, e)
        if fname is None:
            continue

        # create any directories required
        if e.type != Entry.Directory:
            dirname = os.path.dirname(fname)
        else:
            dirname = fname
        os.makedirs(dirname, exist_ok=True)

        data = get_data_object(e)
        if data is not None:
            write_file(fname, data)

action_handlers = {Action.FAIL: do_fail, Action.LIST: do_list, Action.UNPACK: do_unpack}

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="ITEPKG file to work on")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", help="List container elements", action="store_true")
    group.add_argument("-u", "--unpack",
            help="Unpack element of ID to directory (default=-1=all)",
            default=-1, metavar="ID", nargs='?')

    parser.add_argument("-d", "--directory", help="Unpack to DIR, instead of CWD",
            type=str, metavar="DIR")

    args = parser.parse_args()
    action = Action.FAIL
    if args.list == True:
        action = Action.LIST
    elif args.unpack != -1:
        action = Action.UNPACK
        # if unpack given, default to -1
        if args.unpack == None:
            args.unpack = -1

    if args.directory is None:
        args.directory = os.getcwd()

    # open input file and read it
    fp = os.open(args.file, os.O_RDONLY)
    fsize = os.lseek(fp, 0, os.SEEK_END)
    os.lseek(fp, 0, os.SEEK_SET)
    b = os.read(fp, fsize)

    # parse ITEPKG
    pkg, b = itepkg.itepkg.ITEPKG.from_bytes(b)
    if (len(b) > 0):
        print("Superfluous bytes after ITEPKG. Make sure you gave proper ITEPKG file", file=sys.stderr)

    # do selected action
    action_handlers[action](pkg, args)

    # TODO: do stuff

    # cleanup
    os.close(fp)

if __name__ == '__main__':
    main(sys.argv)
