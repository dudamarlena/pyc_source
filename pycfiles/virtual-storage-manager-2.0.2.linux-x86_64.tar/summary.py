# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/summary.py
# Compiled at: 2016-06-13 14:11:03
from vsm.api import common
import logging, json
LOG = logging.getLogger(__name__)
import time

class ViewBuilder(common.ViewBuilder):
    _collection_name = 'summary'

    def basic(self, summary, sum_type):
        dict_root = sum_type + '-summary'
        if not summary:
            return {dict_root: None}
        else:
            if (not summary.get('summary_data')) | (summary.get('summary_data') == 'null'):
                return {dict_root: None}
            try:
                updated_at = summary.get('updated_at').strftime('%Y-%m-%d %H:%M:%S')
            except:
                updated_at = ''

            sum_data = json.loads(summary['summary_data'])
            LOG.debug('summary data: %s' % sum_data)
            if sum_type == 'osd':
                sum_data = sum_data.get('osdmap')
                ret = {dict_root: {'epoch': sum_data.get('epoch', 0), 
                               'num_osds': sum_data.get('num_osds', 0), 
                               'num_up_osds': sum_data.get('num_up_osds', 0), 
                               'num_in_osds': sum_data.get('num_in_osds', 0), 
                               'full': sum_data.get('full', None), 
                               'nearfull': sum_data.get('nearfull', None), 
                               'updated_at': updated_at}}
                LOG.debug('return view %s' % ret)
                return ret
            if sum_type == 'monitor':
                ret = {dict_root: {'monmap_epoch': sum_data.get('monmap_epoch'), 
                               'monitors': sum_data.get('monitors'), 
                               'election_epoch': sum_data.get('election_epoch'), 
                               'quorum': sum_data.get('quorum'), 
                               'overall_status': sum_data.get('overall_status'), 
                               'updated_at': updated_at, 
                               'quorum_leader_name': sum_data.get('quorum_leader_name'), 
                               'quorum_leader_rank': sum_data.get('quorum_leader_rank')}}
                LOG.debug('return view %s' % ret)
                return ret
            if sum_type == 'mds':
                ret = {dict_root: {'epoch': sum_data.get('epoch'), 
                               'num_up_mdses': sum_data.get('up'), 
                               'num_in_mdses': sum_data.get('in'), 
                               'num_max_mdses': sum_data.get('max'), 
                               'num_failed_mdses': sum_data.get('failed'), 
                               'num_stopped_mdses': sum_data.get('stopped'), 
                               'metadata_pool': sum_data.get('metadata_pool'), 
                               'data_pools': sum_data.get('data_pools'), 
                               'updated_at': updated_at}}
                LOG.debug('return view %s' % ret)
                return ret
            if sum_type == 'placement_group':
                ret = {dict_root: {'version': sum_data.get('version'), 
                               'num_pgs': sum_data.get('num_pgs'), 
                               'pgs_by_state': sum_data.get('pgs_by_state'), 
                               'data_bytes': sum_data.get('data_bytes', 0), 
                               'bytes_used': sum_data.get('bytes_used', 0), 
                               'bytes_avail': sum_data.get('bytes_avail', 0), 
                               'bytes_total': sum_data.get('bytes_total', 0), 
                               'degraded_objects': sum_data.get('degraded_objects', 0), 
                               'degraded_total': sum_data.get('degraded_total', 0), 
                               'degraded_ratio': sum_data.get('degraded_ratio', 0), 
                               'unfound_objects': sum_data.get('unfound_objects', 0), 
                               'unfound_total': sum_data.get('unfound_total', 0), 
                               'unfound_ratio': sum_data.get('unfound_ratio', 0), 
                               'read_bytes_sec': sum_data.get('read_bytes_sec', 0), 
                               'write_bytes_sec': sum_data.get('write_bytes_sec', 0), 
                               'op_per_sec': sum_data.get('op_per_sec', 0), 
                               'updated_at': updated_at}}
                LOG.debug('return view %s' % ret)
                return ret
            if sum_type == 'cluster':
                ret = {dict_root: {'cluster': sum_data.get('cluster'), 
                               'status': sum_data.get('status'), 
                               'detail': sum_data.get('detail'), 
                               'health_list': sum_data.get('health_list'), 
                               'updated_at': updated_at}}
                LOG.debug('return view %s' % ret)
                return ret
            if sum_type == 'vsm':
                ret = {dict_root: {'uptime': sum_data.get('uptime'), 
                               'ceph_version': sum_data.get('ceph_version'), 
                               'created_at': sum_data.get('created_at'), 
                               'is_ceph_active': sum_data.get('is_ceph_active'), 
                               'updated_at': updated_at}}
                LOG.debug('return view %s' % ret)
                return ret
            return