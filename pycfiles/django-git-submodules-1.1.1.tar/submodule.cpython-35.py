# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/adere/code/api/django-submodule/django_submodule/submodule.py
# Compiled at: 2016-08-28 15:22:48
# Size of source mod 2**32: 218 bytes
import sys, os, __main__

def add(submodule):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__main__.__file__))
    path = os.path.abspath('{}/{}/'.format(PROJECT_ROOT, submodule))
    sys.path.append(path)