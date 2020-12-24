# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/heccer/__cbi__.py
# Compiled at: 2011-09-09 23:43:09
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
__description__ = '\nHeccer is a fast compartmental solver, that is based on hsolve of the GENESIS simulator.\n\nHeccer can be instantiated from C, or from Perl (or other scripting languages). It is also possible to link Heccer directly to Matlab. Heccer comes with Swig interface definitions, such that linking Heccer to any other technologies should be easy.\nAdding new channel types to Heccer can be done using callouts. The callout mechanism allows for general user extensions that contribute a current or conductance at a particular time in a simulation. Heccer automatically integrates this contribution into the membrane potential. \n\n Heccer is currently capable of simulating Purkinje cells (see the Purkinje Cell Model), and, at first evaluation, runs slightly faster than hsolve (It is difficult to assess why exactly: while the hsolve implementation is much more optimized than Heccer\'s, the Heccer design is slightly better optimized than hsolve\'s.).\n\nHeccer can operate in a "passive-only" mode, i.e. all channels in a model are ignored with exception of the synaptic channels.\nTables to speed up computations, are dynamically generated and optimized.\nAll parts of a model with the same kinetics automatically share tables.\nComputes the contribution of one channel type to the overall dendritic current, e.g. the contribution of all calcium channels or the contribution of all persistent calcium channels.\n.\nHeccer has been validated with a Purkinje cell model and produces an exact match with hsolve (see the purkinje cell model and the Purkinje cell tutorial in the GENESIS simulator distribution). Heccer is constantly undergoing regression tests. \n'
__download_url__ = 'http://repo-genesis3.cbi.utsa.edu'

class PackageInfo:

    def GetRevisionInfo(self):
        return 'b7c5c32cb381e48e57c8383aa8574b40f0aab342'

    def GetName(self):
        return 'heccer'

    def GetVersion(self):
        return '0.0.0-alpha'

    def GetDependencies(self):
        """!
        @brief Provides a list of other CBI dependencies needed.
        """
        dependencies = []
        return dependencies