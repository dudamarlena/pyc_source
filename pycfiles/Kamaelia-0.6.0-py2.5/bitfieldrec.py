# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Data/bitfieldrec.py
# Compiled at: 2008-10-19 12:19:52
"""
Bit Field Record Support
========================

1. subclass bfrec
2. Define a class var "fields"
3. The value for this field should be a list of "field"s, created by calling the static method
   field.mkList. This takes a list of tuples, one tuple per field.
   (fieldname, bitwidth, None or list)

   See  testBFR for an example.

Usage::

   >> import bitfieldrec
   >> bfrec,field = bitfieldrec.bfrec,bitfieldrec.field
   >> reload(bitfieldrec)

Currently only supports packing. Does not support unpacking (yet).
"""
from Axon import AxonObject

class field(str):
    size = 0
    extra = None

    def mkList(fieldDefs):
        result = list()
        for definition in fieldDefs:
            (name, size, extra) = definition
            j = field(name)
            j.size = size
            j.extra = extra
            result.append(j)

        return result

    mkList = staticmethod(mkList)


class bfrec(AxonObject):
    fields = []
    csize = 8

    def __init__(self, **args):
        try:
            self.fields = field.mkList(args['fields'])
        except KeyError:
            pass

        for i in self.fields:
            try:
                self.__dict__[i] = args[i]
            except KeyError:
                if i.extra is list:
                    self.__dict__[i] = []
                else:
                    self.__dict__[i] = 0

    def structureSize(self):
        bits = 0
        for aField in self.fields:
            if aField.extra is list:
                bits = bits + aField.size * len(self.__dict__[aField])
            else:
                bits = bits + aField.size

        return bits

    def pack(self):

        def serialiseable(convert, aField):
            """ Returns an iterable collection of values. (eg list) Either an
         existing one, or puts scalar/singleton values into a list. Doing
         this removes a special case."""
            if aField.extra is not None:
                values = convert[aField]
            else:
                values = [
                 convert[aField]]
            return values

        csize = self.csize
        fields = self.fields
        convert = self.__dict__
        (space, value) = (8, 0)
        r = []
        assert self.structureSize() % csize == 0, 'Structure is not a multiple of packsize'
        for aField in fields:
            fmax = 2 ** aField.size - 1
            values = serialiseable(convert, aField)
            for aValue in values:
                assert 0 <= aValue <= fmax, 'Field value out of range ' + aField + '=' + str(convert[aField]) + ' max' + str(fmax)
                fsize = aField.size
                while fsize:
                    if fsize <= space:
                        data = aValue & 2 ** fsize - 1
                        space = space - fsize
                        value = value + (data << space)
                        fsize = 0
                    else:
                        data = aValue >> fsize - space
                        value = value + data
                        aValue = aValue & 2 ** (fsize - space) - 1
                        fsize = fsize - space
                        space = space - csize
                        if space < 0:
                            space = 0
                    if space == 0:
                        if value > 2 ** csize - 1:
                            raise 'Bad Value', value
                        r.append(value)
                        space = csize
                        value = 0

        return r


if __name__ == '__main__':

    def bin(value, width=8):
        aList = [value]

        def _bin(seq):
            return [
             seq[0] / 2, seq[0] % 2] + seq[1:]

        while aList[0] > 1:
            aList = _bin(aList)

        r = reduce(lambda x, y: x + y, map(lambda x: str(x), aList))
        r = '0' * (width - len(r)) + r
        return r


    class testBFR(bfrec):
        fields = field.mkList([('hello', 4, None),
         ('goodbye', 4, None),
         (
          'Whatever', 5, list),
         ('SoWhat', 32, None),
         ('Bibble', 3, None)])


    a = testBFR(hello=10, goodbye=2, Whatever=[
     10, 10, 10, 10, 10, 10, 10, 10, 10], SoWhat=10, Bibble=7)
    a = testBFR()
    a.hello = 10
    a.goodbye = 2
    a.Whatever = [10, 10, 10, 10, 10, 10, 10, 10, 10]
    a.SoWhat = 10
    a.Bibble = 7
    print a.pack()
    print map(lambda x: bin(x), a.pack())