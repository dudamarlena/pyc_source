# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ccb/Connect.py
# Compiled at: 2012-11-09 16:40:24
"""
Copyright 2012 Oscar Curero

This code is free software; you can redistribute it and/or modify it
under the terms of the GPL 3 license (see the file
COPYING.txt included with the distribution).
"""
from Exceptions import *
from Clearcheckbook import Clearcheckbook
from Utils import sendCommand
from httplib2 import ServerNotFoundError

def Connect(username, password):
    try:
        response = sendCommand('GET', 'premium', None, (username, password))
    except ServerNotFoundError:
        raise ConnectionError()

    if response == 'login failed':
        raise AuthError()
    else:
        return response
    return