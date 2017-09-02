#!/usr/bin/env python3
# classes for entry serialization
from type.uint32 import uint32
from type.vector import vector

class UnknownEntry:

    def __init__(self, unknown1, unknown2):
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

class _FSEntry:

    max32 = 256 ** 4 - 1

    def __init__(self, filename):
        if isinstance(filename, vector):
            self.filename = filename
        else:
            self.filename = vector(0, FileEntry.max32, bytes, filename,
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
    pass

class FileEntry(_FSEntry):

    def __init__(self, filename, contents):
        super().__init__(filename)
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
