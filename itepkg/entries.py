#!/usr/bin/env python3
# classes for entry serialization
from type.uint32 import uint32
from type.vector import vector

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
