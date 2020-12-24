# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klen/Projects/zeta-library/zetalibrary/packer.py
# Compiled at: 2012-08-18 05:47:31
from os import path as op
from sys import stderr, stdout
from zetalibrary.parser import CSSParser, SCSSParser, JSParser
from zetalibrary.settings import LIBDIR
from zetalibrary.utils import color_msg, ZetaError

class Packer(object):

    def __init__(self, path, args):
        self.path = path.rstrip(op.sep)
        self.basedir = op.abspath(op.dirname(path))
        self.args = args
        self.imports = set()
        self.parsers = dict(css=CSSParser(self.basedir, compress=self.args.compress), scss=SCSSParser(self.basedir, compress=self.args.compress), js=JSParser(self.basedir, compress=self.args.compress))

    def pack(self):
        """ Pack and save file """
        pack_name = self.args.prefix + op.basename(self.path)
        pack_path = op.join(self.args.output or self.basedir, pack_name)
        self.out('Packing: %s' % self.path)
        self.out('Output: %s' % pack_path)
        if self.args.format:
            ext = self.get_ext(self.path)
            self.parsers[ext] = self.args.format
        out = ('').join(self.merge(self.parse(self.path)))
        try:
            open(pack_path, 'w').write(out)
            self.out("Linked file saved as: '%s'." % pack_path)
        except IOError as ex:
            raise ZetaError(ex)

    @staticmethod
    def get_ext(path):
        _, ext = op.splitext(path)
        return ext.lstrip('.').lower()

    def get_parser(self, path):
        return self.parsers.get(self.get_ext(path))

    def parse(self, path, parent=None):
        self.imports.add(path)
        parser = self.get_parser(path)
        curdir = op.dirname(path)
        result = []
        try:
            src, imports = parser.parse_path(path)
            for f in filter(lambda x: x not in self.imports, map(lambda x: op.abspath(op.relpath(op.join(curdir, x))), map(lambda x: self.parse_path(x, curdir), imports))):
                result = result + self.parse(f, parent=path)

            result.append((path, parent, parser, src))
        except IOError as e:
            self.out(str(e), error=True)

        self.out(' * %s' % path)
        return result

    def merge(self, tree):
        for path, parent, parser, src in tree:
            src = parser.parse_src(src, path)
            if not src:
                continue
            if not self.args.compress:
                yield parser.comment_template % '=========='
                if parent:
                    from_path = parent.replace(LIBDIR, 'zeta:/') if parent.startswith(LIBDIR) else op.relpath(parent, self.path)
                    yield parser.comment_template % "From: '%s'" % from_path
                target_path = path.replace(LIBDIR, 'zeta:/') if path.startswith(LIBDIR) else op.relpath(path, self.path)
                yield parser.comment_template % "Zeta import: '%s'" % target_path
                yield src
                yield '\n\n'
            else:
                yield src

        yield '\n'

    def parse_path(self, path, curdir):
        """ Normilize path. """
        if path.startswith('http://'):
            return path
        if path.startswith('zeta://'):
            zpath = op.join(LIBDIR, path[len('zeta://'):])
            if self.args.directory and not op.exists(zpath):
                return op.join(self.args.directory, path[len('zeta://'):])
            return zpath
        return op.abspath(op.normpath(op.join(curdir, path)))

    @staticmethod
    def out(msg, error=False):
        """ Send message to shell """
        pipe = stdout
        if error:
            pipe = stderr
            msg = color_msg(msg, 'warning')
        pipe.write('%s\n' % msg)