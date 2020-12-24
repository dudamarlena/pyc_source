# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill2/browser/firefox.py
# Compiled at: 2011-01-13 01:48:00
import os, sys, tempfile
from distutils import dir_util
copytree = dir_util.copy_tree
this_dir = os.path.abspath(os.path.dirname(__file__))
windmill_dir = os.path.abspath(os.path.dirname(this_dir))

def create_extension():
    t = tempfile.mkdtemp(prefix='windmill2.')
    copytree(os.path.join(this_dir, 'extension'), t)
    copytree(os.path.join(windmill_dir, 'castile', 'js'), os.path.join(t, 'resource', 'castile'))
    return t