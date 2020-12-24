# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/chemesis3/__cbi__.py
# Compiled at: 2011-09-09 23:43:12
__doc__ = '\n@file __cbi__.py\n\nThis file provides data for a packages integration\ninto the CBI architecture.\n'
__author__ = 'Mando Rodriguez'
__copyright__ = 'Copyright 2010, The GENESIS Project'
__credits__ = ['Hugo Cornelis', 'Dave Beeman']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Mando Rodriguez'
__email__ = 'rodrigueza14@uthscsa.edu'
__status__ = 'Development'
__url__ = 'http://genesis-sim.org'
__description__ = '\nChemesis3 is a GENESIS3 reimplementation of chemesis from GENESIS. Chemesis3 is a solver\nused to model kinetic and biochemical reaction pathways for GENESIS3.\n'
__download_url__ = 'http://repo-genesis3.cbi.utsa.edu'

class PackageInfo:

    def GetRevisionInfo(self):
        return '40ac0a7a884b8f9a4d9a793c25dcf28ea8eb503a'

    def GetName(self):
        return 'chemesis3'

    def GetVersion(self):
        return '0.0.0-alpha'

    def GetDependencies(self):
        """!
        @brief Provides a list of other CBI dependencies needed.
        """
        dependencies = []
        return dependencies