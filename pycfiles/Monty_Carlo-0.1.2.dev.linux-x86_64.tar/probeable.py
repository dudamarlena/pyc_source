# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/monty-carlo/probes/probeable.py
# Compiled at: 2011-09-10 22:22:14
"""
Probable Class definition
"""
import numpy as num

class probeable_obj:

    def __init__(self):
        self.probes = []

    def attach(self, probe):
        if probe in self.probes:
            print 'This probe is already attached.'
        else:
            self.probes.append(probe)

    def populate_probes(self, subroutine):
        for probe in self.probes:
            if probe.subroutine == subroutine:
                measured = probe.function(self)
                print measured
                probe.data = num.append(probe.data, measured)