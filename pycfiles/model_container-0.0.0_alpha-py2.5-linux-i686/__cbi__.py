# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/model_container/__cbi__.py
# Compiled at: 2011-09-09 23:42:49
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
__description__ = "\nThe Model Container is used as an abstraction layer on top of a simulator and deals with biological entities and end-user concepts instead of mathematical equations. It provides a solver independent internal storage format for models that allows user independent optimizations of the numerical core. By containing the biological model, the Model Container makes the implementation of the numerical core independent of software implementation.\nThe Model Container API abstracts away all the mathematical and computational details of the simulator. Optimized to store large models in little memory it stores neuronal models in a fraction of the memory that would be used by conventional simulators and provides automatic partitioning of the model such that simulations can be run in parallel. From the modeler's perspective, the Model Container will be able to import and export NeuroML files to facilitate model exchange and ideas.\n"
__download_url__ = 'http://repo-genesis3.cbi.utsa.edu'

class PackageInfo:

    def GetRevisionInfo(self):
        return 'c387d0fa6f794c217458406adefa206a5adaeca6'

    def GetName(self):
        return 'model-container'

    def GetVersion(self):
        return '0.0.0-alpha'

    def GetDependencies(self):
        """!
        @brief Provides a list of other CBI dependencies needed.
        """
        dependencies = []
        return dependencies