# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sample/complex_plan/sample_topology.py
# Compiled at: 2015-05-10 11:41:51
from hydro.topology_base import Topology

class SampleTopology(Topology):

    def _submit(self, params):
        """
        topology consists of several steps, defining one source stream or more, combining and transformations
        """
        main_stream = self.query_engine.get('complex_data', params)
        return main_stream