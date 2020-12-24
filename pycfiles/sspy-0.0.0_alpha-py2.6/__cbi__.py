# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mando/neurospaces_project/sspy/source/snapshots/0/build/lib/sspy/__cbi__.py
# Compiled at: 2011-09-15 17:42:41
"""
@file __cbi__.py

This file provides data for a packages integration
into the CBI architecture.
"""
__author__ = 'Mando Rodriguez'
__copyright__ = 'Copyright 2010, The GENESIS Project'
__credits__ = ['Mando Rodriguez', 'Hugo Cornelis', 'Allan Coop']
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'Mando Rodriguez'
__email__ = 'rodrigueza14 at uthscsa.edu'
__requires__ = ['yaml']
__status__ = 'Development'
__description__ = '\nThe simple scheduler in python is a software package that \nuses the model container (a service) and heccer (a solver) to run a simulation \nwith a set of simulation parameters. It can be extended by using and creating \nplugins for solvers, services, inputs and outputs. \n'
__url__ = 'http://genesis-sim.org'
__download_url__ = 'http://repo-genesis3.cbi.utsa.edu'

class PackageInfo:

    def GetRevisionInfo(self):
        return '86a093ecc5d3027ffafe0151ba6c0319bc6b7b83'

    def GetName(self):
        return 'sspy'

    def GetVersion(self):
        return '0.0.0-alpha'

    def GetDependencies(self):
        """!
        @brief Provides a list of other CBI dependencies needed.
        """
        dependencies = []
        return dependencies