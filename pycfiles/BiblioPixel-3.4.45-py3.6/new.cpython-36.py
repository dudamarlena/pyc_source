# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/commands/new.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2765 bytes
"""
Create a new BLiPS project
"""
import os, re, string
from ..util import log
DESCRIPTION = '\nExample:\n\n.. code-block: bash\n\n    # Create a new project directory named my_project/ in the current directory\n    bp new my_project\n\n    # Create a new project directory named my_project/ in ~/projects\n    bp new my_project ~/projects\n\n'
PUNCTUATION = '._'
LEGAL_CHARS = set(string.ascii_letters + string.digits + PUNCTUATION)
DIR_NAME = os.path.dirname(__file__)

def run(args):
    name = args.project_name
    bad = set(name) - LEGAL_CHARS
    if bad:
        raise ValueError('Bad characters in project: "%s"' % ''.join(bad))
    if not name[0].isalpha():
        raise ValueError('Project names must start with a character')
    directory = args.directory or name
    if os.path.exists(directory):
        raise ValueError('Directory "%s" already exists' % directory)
    os.makedirs(directory)
    words = _split_words(name)
    class_name = ''.join(w.capitalize() for w in words)
    py_name = name.replace('.', '_').replace('-', '_')
    context = {'class_name':class_name, 
     'name':name, 
     'py_name':py_name}
    for template, out_file in TEMPLATES.items():
        out_file = (out_file.format)(**context)
        out_file = os.path.join(directory, out_file)
        tmpl_file = os.path.join(DIR_NAME, template)
        tmpl_data = open(tmpl_file).read()
        with open(out_file, 'w') as (fp):
            fp.write((tmpl_data.format)(**context))
            log.printer('Written', out_file)

    log.printer('Created new project in', directory)


def add_arguments(parser):
    parser.set_defaults(run=run)
    parser.add_argument('project_name', help=PROJECT_NAME_HELP)
    parser.add_argument('directory', default='', nargs='?', help=DIRECTORY_HELP)


TEMPLATES = {'template/project.yml.tmpl':'{name}.yml', 
 'template/animation.py.tmpl':'{py_name}.py'}
PROJECT_NAME_HELP = '\nThe Name of the new BLiPS project you want to create.\n\nA Project Name can contain letters, numbers, or `_`. Nothing else is\nallowed, which means no whitespace, "no `/`" and no `.`.\n\nA project name must start with a letter.\n\nValid project names are:\n\n* P\n* project_name\n* IHeartArea51\n\nInvalid project names are:\n\n* 23skidoo\n* project.name\n* _23skidoo\n\n'
DIRECTORY_HELP = '\nOptional directory where you want to create the project.\nIf absent, use the name of the project as the directory name.\n'
_split_words = re.compile('\n    # Find words in a string. Order matters!\n    [A-Z]+(?=[A-Z][a-z]) |  # All upper case before a capitalized word\n    [A-Z]?[a-z]+ |  # Capitalized words / all lower case\n    [A-Z]+ |  # All upper case\n    \\d+  # Numbers\n', re.VERBOSE).findall