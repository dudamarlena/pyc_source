# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/valdergallo/Sandbox/easychain/.env/lib/python2.7/site-packages/easychain/exception.py
# Compiled at: 2018-03-13 08:45:37


class InvalidMessage(Exception):
    """Invalid Message"""
    pass


class InvalidBlock(Exception):
    """Invalid Block"""
    pass


class InvalidBlockchain(Exception):
    """Invalid Blockchain"""
    pass