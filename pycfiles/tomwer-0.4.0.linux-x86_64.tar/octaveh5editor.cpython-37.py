# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/octaveh5editor.py
# Compiled at: 2019-09-12 03:23:33
# Size of source mod 2**32: 2191 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '15/02/2017'

class OctaveH5Editor(object):
    __doc__ = 'Abstract class inheritate by classes which will edit an h5 file'

    def __init__(self):
        """
        """
        self.loadedStructures = None

    def loadReconsParams(self, structures):
        """
        Load h5 structure from the given h5 file

        :param structures: the structures loaded
        """
        self.loadedStructures = structures

    def getLoadedStructures(self):
        """
        :return: the dictionnary of the loaded structure
        """
        return self.loadedStructures

    def getStructs(self):
        """
        :return: the dictionnary of all the h5 structure"""
        raise NotImplementedError('OctaveH5Editor is an abstract class')