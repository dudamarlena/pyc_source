# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzzword/__main__.py
# Compiled at: 2020-05-05 15:51:51
# Size of source mod 2**32: 724 bytes
"""
python -m buzzword
python -m buzzword runserver
python -m buzzword reload
etc
"""
import os, sys, pathlib
from django.core.management import execute_from_command_line
CWD = os.getcwd()
manage_dir = pathlib.Path(__file__).parent.parent.absolute()
os.chdir(manage_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buzzword.settings')
os.environ.setdefault('BUZZWORD_CORPORA_FILE', os.path.join(CWD, 'corpora.json'))
os.environ.setdefault('BUZZWORD_ROOT', CWD)
if len(sys.argv) == 1 and '__main__.py' in sys.argv[0]:
    argv = [
     'manage.py', 'runserver']
else:
    if len(sys.argv) > 1:
        argv = [
         'manage.py', *sys.argv[1:]]
    else:
        argv = sys.argv
execute_from_command_line(argv)