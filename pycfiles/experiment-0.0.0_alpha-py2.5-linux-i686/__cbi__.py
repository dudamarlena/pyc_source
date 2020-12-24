# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/experiment/__cbi__.py
# Compiled at: 2011-09-09 23:42:55
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
__email__ = 'rodrigueza14@uthscsa.edu'
__status__ = 'Development'
__url__ = 'http://genesis-sim.org'
__description__ = '\nThe experiment module houses experimental protocols for use\nin simulations in GENESIS 3. \n'
__download_url__ = 'http://repo-genesis3.cbi.utsa.edu'

class PackageInfo:

    def GetRevisionInfo(self):
        return 'b827606eacc9c544355df892a8244865898ab937'

    def GetName(self):
        return 'experiment'

    def GetVersion(self):
        return '0.0.0-alpha'

    def GetDependencies(self):
        """!
        @brief Provides a list of other CBI dependencies needed.
        """
        dependencies = []
        return dependencies