# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/model/SCOPProteinData.py
# Compiled at: 2009-10-06 08:46:19
__doc__ = '\nA protein SCOP classification.\n'

class SCOPProteinData(object):
    """
    This class must be used to represents the SCOP classification of a protein.
    """

    def __init__(self, data=None):
        """
        Defines the SCOP data.
        
        arguments:
            data: the SCOP data for a classified protein. It is a dictionary with keys the SCOP hierarchical levels.
        """
        if data:
            self.Class = data['Class']
            self.fold = data['Fold']
            self.superfamily = data['Superfamily']
            self.family = data['Family']