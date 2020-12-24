# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/models/intentdef.py
# Compiled at: 2017-10-30 12:01:58
""" Intent definition from a YAML config. """

class IntentDef:
    """ Intent definition from a YAML config. """

    def __init__(self, name, action):
        """ Initialisation.

        :param name: the name of the intent.
        :param action: the code to execute.
        """
        self.name = name
        self.action = action