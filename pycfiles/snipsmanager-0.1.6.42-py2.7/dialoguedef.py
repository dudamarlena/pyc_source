# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanager/models/dialoguedef.py
# Compiled at: 2017-12-13 13:37:31
""" Dialogue definition from a YAML config. """

class DialogueDef:
    """ Dialogue definition from a YAML config. """

    def __init__(self, name, action):
        """ Initialisation.

        :param name: the name of the dialogue event.
        :param action: the code to execute.
        """
        self.name = name
        self.action = action