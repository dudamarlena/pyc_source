# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/setuptools/setuptools/command/register.py
# Compiled at: 2019-02-06 16:42:30
from distutils import log
import distutils.command.register as orig

class register(orig.register):
    __doc__ = orig.register.__doc__

    def run(self):
        try:
            self.run_command('egg_info')
            orig.register.run(self)
        finally:
            self.announce('WARNING: Registering is deprecated, use twine to upload instead (https://pypi.org/p/twine/)', log.WARN)