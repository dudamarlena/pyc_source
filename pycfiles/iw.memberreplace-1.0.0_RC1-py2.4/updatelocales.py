# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/memberreplace/locales/updatelocales.py
# Compiled at: 2009-03-07 19:02:29
"""
i18n files maintenance utility. Please read the README.txt beside this
file.  Portions of this code have been stolen from
PlacelessTranslationService to prevent PYTHONPATH issues
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os, sys, struct, array
from cStringIO import StringIO
from stat import ST_MTIME
from i18ndude.script import rebuild_pot as i18n_rebuild_pot
from i18ndude.script import sync as i18n_sync
DEBUG = True
DOMAIN = 'iw.memberreplace'
EXCLUDED = [
 'profiles', 'tests']
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_POT = '%s.pot' % DOMAIN
MANUAL_POT = '%s-manual.pot' % DOMAIN
if os.path.exists(MANUAL_POT):
    MERGE_OPT = [
     '--merge', MANUAL_POT]
else:
    MERGE_OPT = []
if EXCLUDED:
    EXCLUDED_OPT = '--exclude="%s"' % (' ').join(EXCLUDED)
else:
    EXCLUDED_OPT = ''
PO_FILENAME = '%s.po' % DOMAIN

def main():
    if DEBUG:
        print 'Rebuilding', GENERATED_POT
    argv = [
     'i18ndude', 'rebuild-pot', '--pot', GENERATED_POT, '--create', DOMAIN, MERGE_OPT, EXCLUDED_OPT, ROOT]
    sys.argv = flatten(argv)
    i18n_rebuild_pot()
    if DEBUG:
        print 'Synching', PO_FILENAME, 'files'
    argv = [
     'i18ndude', 'sync', '--pot', GENERATED_POT, find_po_files()]
    sys.argv = flatten(argv)
    i18n_sync()
    if DEBUG:
        print 'Compiling to', PO_FILENAME[:-2] + 'mo', 'files'
    for po_filename in find_po_files():
        mo_filename = po_filename[:-2] + 'mo'
        if not os.path.exists(mo_filename) or os.stat(po_filename)[ST_MTIME] > os.stat(mo_filename)[ST_MTIME]:
            if DEBUG:
                print mo_filename
            po_hdl = file(mo_filename, 'wb')
            po_hdl.write(Msgfmt(po_filename).get())
            po_hdl.close()


def flatten(seq):
    """
    >>> flatten([0, [1, 2, 3], [4, 5, [6, 7]]])
    [0, 1, 2, 3, 4, 5, 6, 7]
    """
    out = []
    for item in seq:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        elif item:
            out.append(item)

    return out


def find_po_files():
    """List of abs paths to .po files"""
    po_files = []
    for (root, dirs, files) in os.walk(THIS_DIR):
        for blacklisted in ('CVS', '.svn'):
            if blacklisted in dirs:
                dirs.remove(blacklisted)

        if PO_FILENAME in files:
            po_files.append(os.path.join(root, PO_FILENAME))

    return po_files


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
        if isinstance(self.po, file):
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


if __name__ == '__main__':
    main()