# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/swsg/utils.py
# Compiled at: 2010-11-29 08:26:31
from functools import partial
from operator import is_
from hashlib import sha256
is_none = partial(is_, None)

def hash_file(filename):
    with open(filename) as (fp):
        text = fp.read()
    return sha256(text).hexdigest()