# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/__init__.py
# Compiled at: 2019-07-31 10:07:57
# Size of source mod 2**32: 2050 bytes
from __future__ import absolute_import, print_function, division
__authors__ = [
 'Jérôme Kieffer']
__license__ = 'MIT'
__date__ = '23/05/2016'
import os as _os, logging as _logging
_logging.getLogger(__name__).addHandler(_logging.NullHandler())
project = _os.path.basename(_os.path.dirname(_os.path.abspath(__file__)))
try:
    from ._version import __date__ as date
    from ._version import version, version_info, hexversion, strictversion
except ImportError:
    pass