# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/w20e/buildoutskel/buildoutskel.py
# Compiled at: 2012-07-05 10:52:05
from paste.script.templates import Template, var
import os
vars = [
 var('type', 'What type of project do you want? [plone|pyramid|django|pycms]')]

class BuildoutSkel(Template):
    _template_dir = './skel/common'
    summary = 'Buildout config files'
    vars = vars

    def write_files(self, command, output_dir, vars):
        """ Override so as to put the files in '.' """
        type_dir = os.path.join(self.module_dir(), './skel/%s' % vars['type'])
        assert os.path.isdir(type_dir)
        Template.write_files(self, command, '.', vars)
        self._template_dir = type_dir
        Template.write_files(self, command, '.', vars)