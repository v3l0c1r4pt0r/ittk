import struct
import sys

class vector:

    def __init__(self, floor, ceiling, type=str, little=False):
        # both endiannesses support
        self.little = little
        if little:
            self._endian = '<'
        else:
            self._endian = '>'

        self.lw = vector._length_width(floor, ceiling)
        self.floor = floor
        self.ceiling = ceiling
        self.array = []
        self.type = type

    def _length_width(floor, ceiling):
        diff = ceiling - floor
        r = diff
        i = 1
        while r // 256 != 0:
            i += 1
            r = r // 256
            m = r % 256
        return i

    def append(self, element):
        if len(self.array) > self.ceiling:
            raise Exception('Maximum number of elements reached')
        if not isinstance(element, self.type):
            raise Exception('Wrong type of element. %s instead of %s' % (
                    type(element).__name__, self.type.__name__))
        self.array.append(element)

    def _length_in_bytes(self):
        length = 0
        for e in self.array:
            length += len(bytes(e))
        return length

    def _length_to_bytes(self):
        length_he = struct.pack("P", self._length_in_bytes())
        if sys.byteorder == 'little' and not self.little: # FIXME: host=le&target=be
            length_be = bytes(reversed(length_he))
            length = length_be[-self.lw:]
        else:
            length_be = length_he
            length = length_be[:self.lw]
        return length

    def _bytes_to_length(b, little=False):
        if sys.byteorder == 'little' and not little: # FIXME: same as above
            revb = reversed(b)
        else:
            revb = b
        length = 0
        mult = 0
        for b in revb:
            length += b * (256**mult)
            mult += 1
        return length

    def __bytes__(self):
        buf = bytes('', encoding='utf-8')
        length = bytes(self._length_to_bytes())
        buf += length
        for e in self.array:
            buf += bytes(e)
        return buf

    def __str__(self):
        strarray = [str(e) for e in self.array]
        return "[" + ",".join(strarray) + "]"

    def __len__(self):
        return len(self.array)

    def from_bytes(floor, ceiling, eltype, b, little=False):
        lw = vector._length_width(floor, ceiling)
        length = b[:lw]
        length = vector._bytes_to_length(length, little)
        b = b[lw:]
        if length == 0:
            return vector(floor, ceiling, eltype), b
        obj = vector(floor, ceiling, eltype, little)
        rest = b[length:]
        b = b[:length]
        while len(b) > 0:
            if eltype == bytes:
                elem = b[:length]
                b = b[length:]
                obj.append(elem)
            else:
                elem, b = eltype.from_bytes(b)
                obj.append(elem)
        return obj, rest
