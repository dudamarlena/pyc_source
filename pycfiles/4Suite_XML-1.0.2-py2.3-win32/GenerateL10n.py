# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\GenerateL10n.py
# Compiled at: 2006-08-11 14:46:52
import os, time
from distutils.core import Command
from distutils.dep_util import newer_group
POT_HEADER = '# %(name)s LANGUAGE message catalog\n# Copyright %(year)s %(author)s\n# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n#\nmsgid ""\nmsgstr ""\n"Project-Id-Version: %(name)s %(version)s\\n"\n"POT-Creation-Date: %(creation-date)s\\n"\n"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n"Language-Team: LANGUAGE <LL@li.org>\\n"\n"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=CHARSET\\n"\n"Content-Transfer-Encoding: ENCODING\\n"\n"Generated-By: %(module)s %(version)s\\n"\n\n'
_escape_chars = None

def _c_escape(s):
    global _escape_chars
    if _escape_chars is None:
        _escape_chars = {'\x00': '\\0', '\x07': '\\a', '\x08': '\\b', '\x0c': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\x0b': '\\v', '"': '\\"'}
        for i in xrange(128, 256):
            _escape_chars[chr(i)] = '\\%03o' % i

    res = list(s)
    for i in xrange(len(res)):
        if _escape_chars.has_key(res[i]):
            res[i] = _escape_chars[res[i]]

    return ('').join(res)
    return


class GenerateL10n(Command):
    __module__ = __name__
    command_name = 'generate_l10n'
    description = 'extract translatable strings from source'
    user_options = [
     (
      'force', 'f', 'force locale generatation (overwrite existing files)')]
    boolean_options = [
     'force']

    def initialize_options(self):
        self.force = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('generate', ('force', 'force'))
        self.translations_dir = 'po'
        return

    def run(self):
        sources = self.get_sources()
        outfile = self.get_pot_filename()
        module_source = os.sep.join(__name__.split('.')) + '.py'
        if os.path.exists(module_source):
            dependencies = sources + [module_source]
        else:
            dependencies = sources
        if not (self.force or newer_group(dependencies, outfile, 'newer')):
            self.announce('skipping catalog generation (up-to-date)', 1)
            return
        messages = self.extract_messages(sources)
        self.write_catalog(messages)
        return

    def extract_messages(self, filenames):
        extractor = Extractor()
        for filename in filenames:
            self.announce('extracting strings from %s' % filename, 1)
            extractor.process(filename)

        return extractor.get_messages()

    def write_catalog(self, messages):

        def normalize(s):
            lines = s.split('\n')
            if len(lines) == 1:
                s = '"' + _c_escape(s) + '"'
            else:
                if not lines[(-1)]:
                    del lines[-1]
                    lines[-1] = lines[(-1)] + '\n'
                for i in range(len(lines)):
                    lines[i] = _c_escape(lines[i])

                lineterm = '\\n"\n"'
                s = '""\n"' + lineterm.join(lines) + '"'
            return s

        self.mkpath(self.translations_dir)
        outfile = self.get_pot_filename()
        self.announce('writing message catalog %s' % outfile, 2)
        if self.dry_run:
            return
        fp = open(outfile, 'wb')
        try:
            timestamp = time.time()
            repl = {'name': self.distribution.get_name(), 'version': self.distribution.get_version(), 'author': self.distribution.get_author(), 'year': time.strftime('%Y', time.localtime(timestamp)), 'creation-date': time.strftime('%Y-%m-%d %H:%M+0000', time.gmtime(timestamp)), 
               'module': __name__}
            print >> fp, POT_HEADER % repl
            for (msgstr, msglocs) in messages:
                isdocstring = 0
                if reduce(operator.__add__, msglocs.values()):
                    isdocstring = 1
                msglocs = msglocs.keys()
                msglocs.sort()
                for (filename, lineno) in msglocs:
                    d = {'filename': filename, 'lineno': lineno}
                    print >> fp, '#: %(filename)s:%(lineno)d' % d

                if isdocstring:
                    print >> fp, '#, docstring'
                print >> fp, 'msgid', normalize(msgstr)
                print >> fp, 'msgstr ""\n'

        finally:
            fp.close()
        return

    def get_sources(self):
        sources = []
        if self.distribution.has_pure_modules():
            cmd = self.get_finalized_command('build_py')
            sources.extend(cmd.get_source_files())
        exclude = os.sep + 'ThirdParty' + os.sep
        sources = [ fn for fn in sources if fn.find(exclude) == -1 ]
        return sources

    def get_pot_filename(self):
        return os.path.join(self.translations_dir, self.distribution.get_name() + '.pot')

    def get_outputs(self):
        if self.distribution.l10n:
            return [
             self.get_pot_filename()]
        return []


import token, tokenize, operator

class Extractor:
    __module__ = __name__

    def __init__(self, excludedStrings=None, keywords=None, docstrings=0):
        self.__excluded = excludedStrings or []
        self.__keywords = ['_']
        if keywords:
            self.__keywords.extend(keywords)
        self.__docstrings = docstrings
        self.__messages = {}
        self.__state = self.__waiting
        self.__data = []
        self.__lineno = -1
        self.__freshmodule = 1
        self.__curfile = None
        return
        return

    def __call__(self, ttype, tstring, stup, etup, line):
        self.__state(ttype, tstring, stup[0])

    def __waiting(self, ttype, tstring, lineno):
        if self.__docstrings:
            if self.__freshmodule:
                if ttype == tokenize.STRING:
                    self.__addentry(eval(tstring), lineno, isdocstring=1)
                    self.__freshmodule = 0
                elif ttype not in (tokenize.COMMENT, tokenize.NL):
                    self.__freshmodule = 0
                return
            if ttype == tokenize.NAME and tstring in ('class', 'def'):
                self.__state = self.__suiteseen
                return
        if ttype == tokenize.NAME and tstring in self.__keywords:
            self.__state = self.__keywordseen

    def __suiteseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == ':':
            self.__state = self.__suitedocstring

    def __suitedocstring(self, ttype, tstring, lineno):
        if ttype == tokenize.STRING:
            self.__addentry(eval(tstring), lineno, isdocstring=1)
            self.__state = self.__waiting
        elif ttype not in (tokenize.NEWLINE, tokenize.INDENT, tokenize.COMMENT):
            self.__state = self.__waiting

    def __keywordseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == '(':
            self.__data = []
            self.__lineno = lineno
            self.__state = self.__openseen
        else:
            self.__state = self.__waiting

    def __openseen(self, ttype, tstring, lineno):
        if ttype == tokenize.OP and tstring == ')':
            if self.__data:
                self.__addentry(('').join(self.__data))
            self.__state = self.__waiting
        elif ttype == tokenize.STRING:
            self.__data.append(eval(tstring))
        elif ttype not in [tokenize.COMMENT, token.INDENT, token.DEDENT, token.NEWLINE, tokenize.NL]:
            print >> sys.stderr, '*** %(file)s:%(lineno)s: Seen unexpected token "%(token)s"' % {'token': tstring, 'file': self.__curfile, 'lineno': self.__lineno}
            self.__state = self.__waiting

    def __addentry(self, msg, lineno=None, isdocstring=0):
        if lineno is None:
            lineno = self.__lineno
        if not msg in self.__excluded:
            entry = (
             self.__curfile, lineno)
            self.__messages.setdefault(msg, {})[entry] = isdocstring
        return

    def process(self, filename):
        self.__curfile = filename
        self.__freshmodule = 1
        fp = open(filename)
        try:
            try:
                tokenize.tokenize(fp.readline, self)
            except tokenize.TokenError, e:
                print >> sys.stderr, '%s: %s, line %d, column %d' % (e[0], filename, e[1][0], e[1][1])

        finally:
            fp.close()
        return

    def get_messages(self):
        messages = []
        reverse = {}
        for (k, v) in self.__messages.items():
            keys = v.keys()
            keys.sort()
            reverse.setdefault(tuple(keys), []).append((k, v))

        rkeys = reverse.keys()
        rkeys.sort()
        for rkey in rkeys:
            rentries = reverse[rkey]
            rentries.sort()
            messages.extend(rentries)

        return messages