# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/djingles/src/djingles/commands/project.py
# Compiled at: 2018-04-18 23:42:54
# Size of source mod 2**32: 499 bytes
import jinja2, os, getpass, shutil, re, click
from .main import cli

def make_dirs(folders):
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


@cli.command()
@click.argument('name')
def start_project(name):
    cwd = os.getcwd()
    src = cwd if os.path.basename(cwd) == 'src' else os.path.join(cwd, 'src')
    base_dir = os.path.dirname(src)
    make_dirs([os.path.join(base_dir, f) for f in ('src', 'etc', 'static', 'media',
                                                   'log', 'data')])