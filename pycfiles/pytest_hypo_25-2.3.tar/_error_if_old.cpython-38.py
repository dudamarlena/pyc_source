# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\_error_if_old.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 998 bytes
import sys
from hypothesis.version import __version__
message = '\nHypothesis {} requires Python 3.5 or later.\n\nThis can only happen if your packaging toolchain is older than python_requires.\nSee https://packaging.python.org/guides/distributing-packages-using-setuptools/\n'
if sys.version_info < (3, 5):
    raise Exception(message.format(__version__))