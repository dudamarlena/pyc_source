# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/setuptools/setuptools/command/register.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 468 bytes
from distutils import log
import distutils.command.register as orig
from setuptools.errors import RemovedCommandError

class register(orig.register):
    __doc__ = 'Formerly used to register packages on PyPI.'

    def run(self):
        msg = 'The register command has been removed, use twine to upload instead (https://pypi.org/p/twine)'
        self.announce('ERROR: ' + msg, log.ERROR)
        raise RemovedCommandError(msg)