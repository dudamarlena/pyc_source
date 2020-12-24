# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/model/CATHProteinData.py
# Compiled at: 2009-10-06 08:44:09
"""
A protein CATH classification.
"""

class CATHProteinData(object):
    """
    This class must be used to represents the CATH classification of a protein.
    """

    def __init__(self, data=None):
        """
        Defines the CATH data.
        
        arguments:
            data: the CATH data for a classified protein. It is a dictionary with keys the CATH hierarchical levels.
        """
        if data:
            self.cath_code = data['CATH code']
            self.Class = data['Class']
            self.architecture = data['Architecture']
            self.topology = data['Topology']
            self.homologous = data['Homologous superfamily']