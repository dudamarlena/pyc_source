# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/mutils.py
# Compiled at: 2017-08-14 14:31:14
import string, random

def genID(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """
        Generate a random ID for creating unique names
        """
    return ('').join(random.choice(chars) for _ in range(size))