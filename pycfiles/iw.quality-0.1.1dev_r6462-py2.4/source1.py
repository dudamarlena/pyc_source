# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/quality/tests/data/source1.py
# Compiled at: 2007-10-12 08:24:06
import compiler, os, logging

def register_module(filename):
    """registers a module"""
    logging.info('Registering %s' % filename)
    CodeSeeker(filename)


def register_folder(folder):
    """walk a folder and register python modules"""
    for (root, dirs, files) in walk(folder):
        for file in files:
            if file.endswith('.py'):
                register_module(os.path.join(root, file))


def enable_log():
    import sys
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console)