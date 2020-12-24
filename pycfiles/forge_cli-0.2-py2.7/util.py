# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/forge/util.py
# Compiled at: 2013-08-16 04:39:31
"""
forge.util
~~~~~

:copyright: (c) 2010-2013 by Luis Morales
:license: BSD, see LICENSE for more details.
"""
import os, sys, inspect

def check_root():
    """
    Check if we have root permissions before starting
    """
    if 'SUDO_UID' not in os.environ.keys():
        print 'This program requires super user priv.'
        sys.exit(1)
    elif os.geteuid() != 0:
        print 'This program requires super user priv.'
        sys.exit(1)


def load_class_from_name(fqcn):
    paths = fqcn.split('.')
    modulename = ('.').join(paths[:-1])
    classname = paths[(-1)]
    __import__(modulename, globals(), locals(), ['*'])
    cls = getattr(sys.modules[modulename], classname)
    if not inspect.isclass(cls):
        raise TypeError('%s is not a class' % fqcn)
    return cls