# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/neurospaces/__cbi__.py
# Compiled at: 2011-09-09 16:55:29
"""
@file __cbi__.py

This file provides data for a packages integration
into the CBI architecture.
"""
__author__ = 'Mando Rodriguez'
__copyright__ = 'Copyright 2010, The GENESIS Project'
__credits__ = ['Hugo Cornelis', 'Dave Beeman']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Mando Rodriguez'
__email__ = 'rodrigueza14 at uthscsa dot edu'
__status__ = 'Development'
__url__ = 'http://genesis-sim.org'
__description__ = "\nThis is the root management module for GENESIS. GENESIS is composed of several\nsub packages for reading and storing models, solvers, experimental protocols,\nand GUI interfaces. The root 'neurospaces' package helps to determine which versions of\npackages are installed and performs updates, removal, and installation of needed\npackages to run a simulation. \n"
__download_url__ = 'http://repo-genesis3.cbi.utsa.edu'

class PackageInfo:

    def GetRevisionInfo(self):
        return '609ee575e9b994be615e017461dd894e0e03fd66'

    def GetName(self):
        return 'neurospaces'

    def GetVersion(self):
        return '0.0.0-alpha'

    def GetDependencies(self):
        """!
        @brief Provides a list of other CBI dependencies needed.
        """
        dependencies = []
        return dependencies