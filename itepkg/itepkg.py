#!/usr/bin/env python3
# module for handling ITEPKG03 file format
from itepkg.exceptions import *
from itepkg.entries import *

class ITEPKG:

    magic = b'ITEPKG03'
    header_length = 0x40

    def __init__(self, header, checksum=0):
        self.magic = ITEPKG.magic

        if isinstance(header, bytes):
            self.header = header
        else:
            self.header = bytes(header)

        if len(self.header) != (ITEPKG.header_length - len(self.magic)):
            raise Exception('Wrong length of header: %d' % len(self.header))

        self.entries = []
        self.checksum = uint32(checksum)

    def append(self, entry):
        self.entries.append(entry)

    def __bytes__(self):
        entries = b''
        for e in self.entries:
            entries += bytes(e)
        return self.magic + self.header + entries

    def __str__(self):
        entries = ', '.join([str(e) for e in self.entries])
        return '{magic = %s, unknown = %s, entries = [%s]}' % (self.magic,
                self.header, entries)

    def __repr__(self):
        raise Exception('Not implemented')

    def __len__(self):
        return len(bytes(self))

    def from_bytes(b):
        magic, b = b[:len(ITEPKG.magic)], b[len(ITEPKG.magic):]
        if magic != ITEPKG.magic:
            raise ParsingException('Wrong magic: %s' % magic)
        hdrlen = ITEPKG.header_length - len(ITEPKG.magic)
        header, b = b[:hdrlen], b[hdrlen:]
        obj = ITEPKG(header)

        entry_type = None
        while len(b) > 0 and entry_type is not Entry.End:
            entry_type, b = Entry.from_bytes(b)
            entry, b = entry_types[entry_type].from_bytes(b)
            obj.append(entry)

        checksum, b = uint32.from_bytes(b)
        obj.checksum = checksum

        return obj, b
