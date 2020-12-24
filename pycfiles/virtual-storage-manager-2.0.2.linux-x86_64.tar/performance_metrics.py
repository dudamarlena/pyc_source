# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/performance_metrics.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging
LOG = logging.getLogger(__name__)

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'performance_metrics'

    def basic(self, performance_metrics):
        return performance_metrics

    def index(self, performance_metrics):
        """Show a list of performance_metrics without many details."""
        return self._list_view(self.basic, performance_metrics)

    def _list_view(self, func, performance_metrics):
        """Provide a view for a list of performance_metrics."""
        performance_metrics_list = [ func(metric)['metric'] for metric in performance_metrics ]
        performance_metrics_dict = dict(performance_metrics=performance_metrics_list)
        return performance_metrics_dict