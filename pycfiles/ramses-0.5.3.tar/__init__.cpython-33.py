# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathan/Documents/workspace/ramses/ramses/scaffolds/__init__.py
# Compiled at: 2016-05-05 17:47:37
# Size of source mod 2**32: 1082 bytes
import os, subprocess
from six import moves
from pyramid.scaffolds import PyramidTemplate

class RamsesStarterTemplate(PyramidTemplate):
    _template_dir = 'ramses_starter'
    summary = 'Ramses starter'

    def pre(self, command, output_dir, vars):
        dbengine_choices = {'1': 'sqla',  '2': 'mongodb'}
        vars['engine'] = dbengine_choices[(moves.input("\n        Which database backend would you like to use:\n\n        (1) for SQLAlchemy/PostgreSQL, or\n        (2) for MongoEngine/MongoDB?\n\n        [default is '1']: ") or '1')]
        if vars['package'] == 'site':
            raise ValueError('\n                "Site" is a reserved keyword in Python.\n                 Please use a different project name. ')

    def post(self, command, output_dir, vars):
        os.chdir(str(output_dir))
        subprocess.call('pip install -r requirements.txt', shell=True)
        subprocess.call('pip install nefertari-{}'.format(vars['engine']), shell=True)
        msg = 'Goodbye boilerplate! Welcome to Ramses.'
        self.out(msg)