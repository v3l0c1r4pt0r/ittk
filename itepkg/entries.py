#!/usr/bin/env python3
# classes for entry serialization
from enum import IntEnum
from type.uint32 import uint32
from type.vector import vector

class Entry(IntEnum):
    End = 0x00
    Memory = 0x03
    Unknown = 0x04
    Directory = 0x05
    File = 0x06

    def from_bytes(b):
        entry, b = uint32.from_bytes(b, little=True)
        return Entry(entry.integer), b

class GenericEntry:

    def __init__(self):
        raise Exception('Cannot instantiate GenericEntry')


class EndEntry(GenericEntry):

    def __init__(self):
        self.type = Entry.End

    def __bytes__(self):
        return b''

    def __str__(self):
        return '{}'

    def __len__(self):
        return 0

    def from_bytes(b):
        return EndEntry(), b


class MemoryEntry(GenericEntry):

    def __init__(self, address, content):
        self.type = Entry.Memory
        if isinstance(address, uint32):
            self.address = address
        else:
            self.address = uint32(address, little=True)

        if isinstance(content, bytes):
            self.content = content
        else:
            self.content = bytes(content)

    def __bytes__(self):
        length = uint32(len(self.content), little=True)
        return bytes(self.address) + bytes(length) + self.content

    def __str__(self):
        return '{address = 0x%x, length = %s, content = %s}' % (
                self.address.integer, len(self.content), self.content)

    def __len__(self):
        return len(bytes(self))

    def from_bytes(b):
        address, b = uint32.from_bytes(b, little=True)
        length, b = uint32.from_bytes(b, little=True)
        content, b = b[:length.integer], b[length.integer:]
        return MemoryEntry(address, content), b


class UnknownEntry(GenericEntry):

    def __init__(self, unknown1, unknown2):
        self.type = Entry.Unknown
        if isinstance(unknown1, uint32):
            self.unknown1 = unknown1
        else:
            self.unknown1 = uint32(unknown1, little=True)

        if isinstance(unknown2, uint32):
            self.unknown2 = unknown2
        else:
            self.unknown2 = uint32(unknown2, little=True)

    def __bytes__(self):
        return bytes(self.unknown1) + bytes(self.unknown2)

    def __str__(self):
        return '{unknown1 = %s, unknown2 = %s}' % (self.unknown1, self.unknown2)

    def __len__(self):
        return len(bytes(self))

    def from_bytes(b):
        unknown1, b = uint32.from_bytes(b, little=True)
        unknown2, b = uint32.from_bytes(b, little=True)
        return UnknownEntry(unknown1, unknown2), b


class _FSEntry(GenericEntry):

    max32 = 256 ** 4 - 1

    def __init__(self, filename):
        self.type = -1
        if isinstance(filename, vector):
            self.filename = filename
        else:
            self.filename = vector(0, _FSEntry.max32, bytes, filename,
                    little=True)

    def __bytes__(self):
        filename = bytes(self.filename)
        return filename

    def __str__(self):
        filename = self.filename.array[0][:-1].decode('utf-8')
        return '{filename = %s}' % (repr(filename))

    def __len__(self):
        return len(bytes(self))

    def from_bytes(b):
        filename, b = vector.from_bytes(0, _FSEntry.max32, bytes, b,
                little=True)
        return _FSEntry(filename), b


class DirectoryEntry(_FSEntry):

    def __init__(self, filename):
        super().__init__(filename)
        self.type = Entry.Directory

    def from_bytes(b):
        filename, b = vector.from_bytes(0, FileEntry.max32, bytes, b,
                little=True)
        return DirectoryEntry(filename), b


class FileEntry(_FSEntry):

    def __init__(self, filename, contents):
        super().__init__(filename)
        self.type = Entry.File
        if isinstance(contents, vector):
            self.contents = contents
        else:
            self.contents = vector(0, FileEntry.max32, bytes, contents,
                    little=True)

    def __bytes__(self):
        return super().__bytes__() + bytes(self.contents)

    def __str__(self):
        filename = self.filename.array[0][:-1].decode('utf-8')
        return '{filename = %s, file = %s}' % (repr(filename), self.contents.array[0])

    def from_bytes(b):
        filename, b = vector.from_bytes(0, FileEntry.max32, bytes, b,
                little=True)
        contents, b = vector.from_bytes(0, FileEntry.max32, bytes, b,
                little=True)
        return FileEntry(filename, contents), b

entry_types = {Entry.End: EndEntry, Entry.Memory: MemoryEntry, Entry.Unknown:
        UnknownEntry, Entry.Directory: DirectoryEntry,
        Entry.File: FileEntry}
