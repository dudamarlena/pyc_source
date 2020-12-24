# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sample/geo_queries/geo_widget_topology.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'moshebasanchig'
from hydro.topology_base import Topology

class GeoWidgetTopology(Topology):

    def _submit(self, params):
        """
        topology consists of several steps, defining one source stream or more, combining and transformations
        """
        main_stream = self.query_engine.get('geo_widget', params)
        lookup_stream = self.query_engine.get('geo_lookup', params, cache_ttl=1)
        combined = self.transformers.combine(main_stream, lookup_stream, left_on=['user_id'], right_on=['user_id'])
        aggregated = self.transformers.aggregate(combined, group_by=['country'], operators={'revenue': 'sum', 'spend': 'sum'})
        aggregated['ROI'] = aggregated.revenue / (aggregated.spend + aggregated.revenue)
        return aggregated