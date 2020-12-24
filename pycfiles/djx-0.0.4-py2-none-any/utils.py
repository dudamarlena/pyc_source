# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/setuptools/setuptools/_vendor/packaging/utils.py
# Compiled at: 2019-02-06 16:42:30
from __future__ import absolute_import, division, print_function
import re
_canonicalize_regex = re.compile('[-_.]+')

def canonicalize_name(name):
    return _canonicalize_regex.sub('-', name).lower()