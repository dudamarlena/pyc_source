# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vandercf/git/atramhasis/atramhasis/scaffolds/__init__.py
# Compiled at: 2017-06-22 05:19:07
from textwrap import dedent
from pyramid.scaffolds import PyramidTemplate, Template
import os, distutils.dir_util

def copy_dir_to_scaffold(output_dir, package, dir):
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', dir))
    dest_dir = os.path.join(output_dir, package, dir)
    distutils.dir_util.copy_tree(source_dir, dest_dir)


class AtramhasisTemplate(PyramidTemplate):
    _template_dir = 'atramhasis_scaffold'
    summary = 'Create an Atramhasis implementation'

    def post(self, command, output_dir, vars):
        """ Overrides :meth:`pyramid.scaffolds.template.Template.post`"""
        copy_dir_to_scaffold(output_dir, vars['package'], 'locale')
        separator = '=' * 79
        msg = dedent('\n            %(separator)s\n            Documentation: http://atramhasis.readthedocs.io\n\n            Welcome to Atramhasis.\n            %(separator)s\n        ' % {'separator': separator})
        self.out(msg)


class AtramhasisDemoTemplate(PyramidTemplate):
    _template_dir = 'atramhasis_demo'
    summary = 'Create an Atramhasis demo'

    def post(self, command, output_dir, vars):
        """ Overrides :meth:`pyramid.scaffolds.template.Template.post`"""
        copy_dir_to_scaffold(output_dir, vars['package'], 'locale')
        separator = '=' * 79
        msg = dedent('\n            %(separator)s\n            Documentation: http://atramhasis.readthedocs.io\n            Demo instructions: http://atramhasis.readthedocs.io/en/latest/demo.html\n\n            Welcome to Atramhasis Demo.\n            %(separator)s\n        ' % {'separator': separator})
        self.out(msg)
        return Template.post(self, command, output_dir, vars)