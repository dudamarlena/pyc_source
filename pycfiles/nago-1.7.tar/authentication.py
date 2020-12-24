# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/palli/workspace/nago/nago/authentication.py
# Compiled at: 2013-11-07 09:35:23
import os, string
__author__ = 'palli'

def generate_token():
    """ Generate a new random security token.

     >>> len(generate_token()) == 50
     True

     Returns:
       string
    """
    length = 50
    stringset = string.ascii_letters + string.digits
    token = ('').join([ stringset[(i % len(stringset))] for i in [ ord(x) for x in os.urandom(length) ] ])
    return token