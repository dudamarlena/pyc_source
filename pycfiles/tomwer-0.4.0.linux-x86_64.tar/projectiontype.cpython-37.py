# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/axis/projectiontype.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 1625 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '15/10/2019'
try:
    import silx.utils.enum as _Enum
except ImportError:
    import tomwer.third_party.enum as _Enum

class ProjectionType(_Enum):
    __doc__ = 'Type of projection'
    transmission = 'transmission'
    absorption = 'absorption'