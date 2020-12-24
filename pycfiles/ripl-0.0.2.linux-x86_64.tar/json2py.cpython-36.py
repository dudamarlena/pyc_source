# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/json2py.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 319 bytes
"""
Take a json string and turn it into python.

Result should be a list of dictionaries or a dictionary of lists or
whatever, per the json input.

World's simplest interpreter.
"""
import json

class Json2Py:

    def interpret(self, msg):
        return json.loads(msg)


x = Json2Py()
interpret = x.interpret