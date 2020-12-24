# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/msgfmt.py
# Compiled at: 2008-04-29 08:14:25
"""Generate binary message catalog from textual translation description.

This program converts a textual Uniforum-style message catalog (.po file) into
a binary GNU catalog (.mo file).  This is essentially the same function as the
GNU msgfmt program, however, it is a simpler implementation.

This file was taken from Python-2.3.2/Tools/i18n and altered in several ways.
Now you can simply use it from another python module:

  from msgfmt import Msgfmt
  mo = Msgfmt(po).get()

where po is path to a po file as string, an opened po file ready for reading or
a list of strings (readlines of a po file) and mo is the compiled mo
file as binary string.

Exceptions:

  * IOError if the file couldn't be read

  * msgfmt.PoSyntaxError if the po file has syntax errors

"""
import struct, array, types
from cStringIO import StringIO
__version__ = '1.1pts'

class PoSyntaxError(Exception):
    """ Syntax error in a po file """
    __module__ = __name__

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Po file syntax error: %s' % self.msg


class Msgfmt:
    """ """
    __module__ = __name__

    def __init__(self, po, name='unknown'):
        self.po = po
        self.name = name
        self.messages = {}

    def readPoData(self):
        """ read po data from self.po and store it in self.poLines """
        output = []
        if isinstance(self.po, types.FileType):
            self.po.seek(0)
            output = self.po.readlines()
        if isinstance(self.po, list):
            output = self.po
        if isinstance(self.po, str):
            output = open(self.po, 'rb').readlines()
        if not output:
            raise ValueError, 'self.po is invalid! %s' % type(self.po)
        return output

    def add(self, id, str, fuzzy):
        """Add a non-empty and non-fuzzy translation to the dictionary."""
        if str and not fuzzy:
            self.messages[id] = str

    def generate(self):
        """Return the generated output."""
        keys = self.messages.keys()
        keys.sort()
        offsets = []
        ids = strs = ''
        for id in keys:
            offsets.append((len(ids), len(id), len(strs), len(self.messages[id])))
            ids += id + '\x00'
            strs += self.messages[id] + '\x00'

        output = ''
        keystart = 7 * 4 + 16 * len(keys)
        valuestart = keystart + len(ids)
        koffsets = []
        voffsets = []
        for (o1, l1, o2, l2) in offsets:
            koffsets += [l1, o1 + keystart]
            voffsets += [l2, o2 + valuestart]

        offsets = koffsets + voffsets
        output = struct.pack('Iiiiiii', 2500072158, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0)
        output += array.array('i', offsets).tostring()
        output += ids
        output += strs
        return output

    def get(self):
        """ """
        ID = 1
        STR = 2
        section = None
        fuzzy = 0
        lines = self.readPoData()
        lno = 0
        for l in lines:
            lno += 1
            if (l[0] == '#' or l.startswith('msgid')) and section == STR:
                self.add(msgid, msgstr, fuzzy)
                section = None
                fuzzy = 0
            if l[:2] == '#,' and 'fuzzy' in l:
                fuzzy = 1
            if l[0] == '#':
                continue
            if l.startswith('msgid'):
                section = ID
                l = l[5:]
                msgid = msgstr = ''
            elif l.startswith('msgstr'):
                section = STR
                l = l[6:]
            l = l.strip()
            if not l:
                continue
            try:
                l = eval(l, globals())
            except Exception, msg:
                raise PoSyntaxError('%s (line %d of po file %s): \n%s' % (msg, lno, self.name, l))

            if section == ID:
                msgid += l
            elif section == STR:
                msgstr += l
            else:
                raise PoSyntaxError('error in line %d of po file %s' % (lno, self.name))

        if section == STR:
            self.add(msgid, msgstr, fuzzy)
        return self.generate()

    def getAsFile(self):
        return StringIO(self.get())

    def __call__(self):
        return self.getAsFile()