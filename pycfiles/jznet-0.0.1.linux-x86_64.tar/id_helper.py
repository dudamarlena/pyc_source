# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pyjznet/id_helper.py
# Compiled at: 2014-12-12 03:14:29
from __future__ import print_function
import uuid

def generate_request_id():
    return str(uuid.uuid4())