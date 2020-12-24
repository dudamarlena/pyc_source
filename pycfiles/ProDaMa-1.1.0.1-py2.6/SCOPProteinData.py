# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/model/SCOPProteinData.py
# Compiled at: 2009-10-06 08:46:19
"""
A protein SCOP classification.
"""

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