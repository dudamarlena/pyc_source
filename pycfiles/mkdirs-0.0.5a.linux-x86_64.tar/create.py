# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mkdirs/create.py
# Compiled at: 2014-10-01 14:16:05
import logging, sys, os
from distutils.dir_util import mkpath
from cliff.command import Command
from templates.template import *

class Create(Command):
    log = logging.getLogger(__name__)

    @staticmethod
    def mkdirp(directory):
        """Creates an empty directory. Python implementation of mkdir"""
        if not os.path.isdir(directory):
            mkpath(directory)

    @staticmethod
    def touch(fname):
        """Creates an empty file. Python implementation of touch"""
        if os.path.exists(fname):
            os.utime(fname, None)
        else:
            open(fname, 'w').close()
        return

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('projectname', metavar='projectname', help='projectname', type=str)
        parser.add_argument('modulename', metavar='modulename', help='modulename', type=str)
        parser.add_argument('authorname', metavar='authorname', help='authorname', type=str)
        parser.add_argument('email', metavar='email', help='email', type=str)
        return parser

    def take_action(self, parsed_args):
        """Override take_action to create and write to files"""
        project_files = [
         'setup.py', 'setup.cfg', 'README.rst']
        module_files = ['__init__.py', 'main.py']
        self.mkdirp(parsed_args.projectname)
        self.mkdirp('%s/%s' % (parsed_args.projectname, parsed_args.modulename))
        for f in project_files:
            self.touch('%s/%s' % (parsed_args.projectname, f))

        for f in module_files:
            self.touch('%s/%s/%s' % (parsed_args.projectname, parsed_args.modulename, f))

        with open(parsed_args.projectname + '/' + 'setup.cfg', 'w') as (f):
            f.write('[bdist_wheel]\n')
            f.write('universal=1\n')
        with open('%s/%s' % (parsed_args.projectname, 'setup.py'), 'w') as (f):
            context = {'modulename': parsed_args.modulename, 'projectname': parsed_args.projectname, 
               'authorname': parsed_args.authorname, 
               'email': parsed_args.email}
            f.write(TEMPLATE_SETUP.format(**context))
            f.write('\n')
            f.write('    entry_points={\n')
            f.write("        'console_scripts':[\n")
            f.write("            '" + parsed_args.modulename + ' = ' + parsed_args.modulename + ".main:main'\n")
            f.write('        ],\n')
            f.write("        '" + parsed_args.modulename + ".app':[\n")
            f.write("            'simple = cliffdemo.simple:Simple',\n")
            f.write('        ],\n')
            f.write('    },\n')
            f.write(')')
        with open('%s/%s/%s' % (parsed_args.projectname, parsed_args.modulename, 'main.py'), 'w') as (f):
            context = {'modulename': parsed_args.modulename.title(), 'modulename_lower': parsed_args.modulename}
            f.write(TEMPLATE_MAIN.format(**context))