# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/model/CATHProteinData.py
# Compiled at: 2009-10-06 08:44:09
__doc__ = '\nA protein CATH classification.\n'

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