# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\BuildL10n.py
# Compiled at: 2006-08-11 14:46:52
import os, glob, struct, array
from distutils import dep_util
from distutils.core import Command
from distutils.errors import DistutilsFileError

class BuildL10n(Command):
    __module__ = __name__
    command_name = 'build_l10n'
    description = 'compile message catalog to binary format'
    user_options = [
     (
      'build-dir=', 'd', 'directory to "build" (copy) to'), ('force', 'f', 'forcibly build everything (ignore file timestamps')]

    def initialize_options(self):
        self.build_dir = None
        self.force = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('build', (
         'build_l10n', 'build_dir'), (
         'force', 'force'))
        self.localizations = self.distribution.l10n
        return

    def run(self):
        domain = self.distribution.get_name()
        for loc in self.localizations:
            build_dir = os.path.join(self.build_dir, loc.language, 'LC_MESSAGES')
            self.mkpath(build_dir)
            pofile = loc.source
            mofile = os.path.join(build_dir, domain + '.mo')
            if not (self.force or dep_util.newer(pofile, mofile)):
                self.announce('not compiling %s (up-to-date)' % pofile, 1)
                continue
            self.announce('compiling %s -> %s' % (pofile, mofile), 2)
            msgfmt = MsgFmt()
            msgfmt.parse(pofile)
            if not self.dry_run:
                fp = open(mofile, 'wb')
                try:
                    msgfmt.generate(fp)
                finally:
                    fp.close()

        return

    def get_outputs(self):
        outputs = []
        domain = self.distribution.get_name()
        for loc in self.localizations:
            build_dir = os.path.join(self.build_dir, loc.language, 'LC_MESSAGES')
            mofile = os.path.join(build_dir, domain + '.mo')
            outputs.append(mofile)

        return outputs

    def get_source_files(self):
        return [ loc.source for loc in self.localizations ]


class MsgFmt:
    __module__ = __name__

    def __init__(self):
        self.__messages = {}
        return

    def add(self, id, str, fuzzy):
        """Add a non-fuzzy translation to the dictionary."""
        if not fuzzy and str:
            self.__messages[id] = str

    def generate(self, fp):
        """Return the generated output."""
        keys = self.__messages.keys()
        keys.sort()
        offsets = []
        ids = strs = ''
        for id in keys:
            msgstr = self.__messages[id]
            offsets.append((len(ids), len(id), len(strs), len(msgstr)))
            ids += id + '\x00'
            strs += msgstr + '\x00'

        keystart = 7 * 4 + 16 * len(keys)
        valuestart = keystart + len(ids)
        koffsets = []
        voffsets = []
        for (o1, l1, o2, l2) in offsets:
            koffsets += [l1, o1 + keystart]
            voffsets += [l2, o2 + valuestart]

        offsets = koffsets + voffsets
        fp.write(struct.pack('Iiiiiii', 2500072158, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0))
        fp.write(array.array('i', offsets).tostring())
        fp.write(ids)
        fp.write(strs)
        return

    def parse(self, pofile):
        ID = 1
        STR = 2
        try:
            lines = open(pofile).readlines()
        except IOError, (errno, errstr):
            raise DistutilsFileError("could not read from '%s': %s" % (pofile, errstr))

        section = None
        fuzzy = 0
        lno = 0
        for l in lines:
            lno += 1
            if l[0] == '#' and section == STR:
                self.add(msgid, msgstr, fuzzy)
                section = None
                fuzzy = 0
            if l[:2] == '#,' and l.find('fuzzy'):
                fuzzy = 1
            if l[0] == '#':
                continue
            if l.startswith('msgid'):
                if section == STR:
                    self.add(msgid, msgstr, fuzzy)
                section = ID
                l = l[5:]
                msgid = msgstr = ''
            elif l.startswith('msgstr'):
                section = STR
                l = l[6:]
            l = l.strip()
            if not l:
                continue
            l = eval(l)
            if section == ID:
                msgid += l
            elif section == STR:
                msgstr += l
            else:
                self.warn('Syntax error on %s:%d before: %s ' % (pofile, lno, l))
                return

        if section == STR:
            self.add(msgid, msgstr, fuzzy)
        return
        return