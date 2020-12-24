# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/cosas/avython/avython/download/wget.py
# Compiled at: 2017-02-05 16:31:12
# Size of source mod 2**32: 204 bytes
from __future__ import absolute_import
from avython.download.driver import BaseDriver

class Driver(BaseDriver):
    command_to_get = 'wget -t 3 {} -O {}'