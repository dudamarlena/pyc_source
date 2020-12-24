# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/w20e/pycms/sitemaker/pycmsbuildouttemplate.py
# Compiled at: 2011-11-01 07:26:05
from paste.script.templates import Template, var
vars = [
 var('pycms_project_path', 'Path to your PyCMS project')]

class PyCMSBuildoutTemplate(Template):
    _template_dir = './buildout_skel'
    summary = 'PyCMS buildout template'
    vars = vars

    def write_files(self, command, output_dir, vars):
        """ Override so as to put the files in '.' """
        Template.write_files(self, command, '.', vars)