# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wikir/commands.py
# Compiled at: 2009-03-26 18:20:42
import os, sys
from setuptools import Command
import pkg_resources
from distutils import log
log.set_threshold(6)
from wikir import split_doc_from_module
from docutils.parsers.rst import directives
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class publish_wiki(Command):
    description = 'Publish RST to wiki'
    user_options = [
     ('source=', 's', 'path to RST source.  if a python module, the top-most docstring will be used as the source')]

    def initialize_options(self):
        self.source = None
        self.input = None
        return

    def finalize_options(self):
        if self.source is None:
            raise NotImplementedError('empty --source, need to iter entry_point')
        if self.source.endswith('.py'):
            (short_desc, long_desc) = split_doc_from_module(self.source)
            self.input = StringIO(long_desc)
        else:
            self.input = open(self.source, 'r')
        return

    def run(self):
        from wikir import publish_file
        for ep in pkg_resources.iter_entry_points('wikir.rst_directives'):
            log.info('registering RST directive: %s', str(ep))
            directives.register_directive(ep.name, ep.load())

        publish_file(self.input)