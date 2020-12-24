# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/command/etags.py
# Compiled at: 2007-08-08 19:58:56
__doc__ = '\nGenerate TAGS file.\n\nThis command is most useful for Emacs users (although other tools read TAGS\nfiles now too).\n'
from distutils.cmd import Command

class etags(Command):
    __module__ = __name__
    description = 'generate Emacs TAGS file.'
    user_options = [
     ('command=', 'c', 'the etags command [default: etags]'), ('tags-file=', 't', 'where to write the TAGS file [default: TAGS]'), ('force', 'f', "force generation of TAGS file even if source files haven't changed")]
    boolean_options = [
     'force']

    def initialize_options(self):
        self.command = 'etags'
        self.tags_file = 'TAGS'

    def finalize_options(self):
        self.ensure_string('command')
        self.ensure_string('tags_file')

    def run(self):
        from distutils.command.build_py import build_py
        base = build_py(self.distribution)
        base.initialize_options()
        base.finalize_options()
        files = base.get_source_files()

        def run_etags():
            args = [self.command, '-lpython', '-o%s' % self.tags_file]
            args += files
            self.spawn(args)

        self.make_file(files, self.tags_file, run_etags, (), exec_msg='tagging (%d) files...' % len(files))