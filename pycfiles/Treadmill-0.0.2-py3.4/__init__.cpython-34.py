# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/__init__.py
# Compiled at: 2017-04-11 07:05:33
# Size of source mod 2**32: 952 bytes
"""Treadmill module."""
import os, pkgutil, treadmill
__path__ = pkgutil.extend_path(__path__, __name__)

def __root_join(*path):
    """Joins path with location of the current file."""
    mydir = os.path.dirname(os.path.realpath(__file__))
    return os.path.realpath(os.path.join(mydir, *path))


if os.name == 'nt':
    _TREADMILL_SCRIPT = 'treadmill.cmd'
else:
    _TREADMILL_SCRIPT = 'treadmill'
VIRTUAL_ENV = os.environ.get('VIRTUAL_ENV')
if VIRTUAL_ENV:
    TREADMILL_BIN = os.path.join(VIRTUAL_ENV, 'bin', _TREADMILL_SCRIPT)
    TREADMILL = os.path.join(treadmill.__path__[0], '../')
else:
    TREADMILL_BIN = os.path.join('/bin', _TREADMILL_SCRIPT)
    TREADMILL = __root_join('..')
TREADMILL_LDAP = os.environ.get('TREADMILL_LDAP')
TREADMILL_DEPLOY_PACKAGE = os.path.join(treadmill.__path__[0], '../deploy/')