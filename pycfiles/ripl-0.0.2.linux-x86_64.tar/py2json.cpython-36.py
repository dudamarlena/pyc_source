# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/py2json.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 225 bytes
"""
Take a python object and turn it into json.

World's simplest interpreter.
"""
import json

class Py2Json:

    def interpret(self, msg):
        return json.dumps(msg, indent=4)


x = Py2Json()
interpret = x.interpret