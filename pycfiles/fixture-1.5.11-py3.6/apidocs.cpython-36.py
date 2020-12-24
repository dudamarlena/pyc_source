# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/setup_cmd/apidocs.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1213 bytes
from distutils.cmd import Command
import os, sys, shutil
from os import path
import optparse
from fixture import docs
from fixture.test import teardown_examples
from docutils.core import publish_file, publish_string, publish_doctree, publish_from_doctree

class apidocs(Command):
    description = 'create API documentation'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """build API documentation."""
        if not path.exists(docs.builddir):
            os.mkdir(docs.builddir)
        docs.state_is_api = True
        from pydoctor.driver import main
        argv = [
         '--html-output=%s/apidocs' % docs.builddir, '--project-name=fixture',
         '--docformat=restructuredtext',
         '--project-url=http://code.google.com/p/fixture/', '--make-html',
         '--add-package=fixture', '--verbose', '--verbose']
        sys.argv[0] = [
         'pydoctor']
        main(argv)