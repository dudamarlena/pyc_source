# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/limits.py
# Compiled at: 2016-06-13 14:11:03
import datetime
from vsm.openstack.common import timeutils

class ViewBuilder(object):
    """OpenStack API base limits view builder."""

    def build(self, rate_limits, absolute_limits):
        rate_limits = self._build_rate_limits(rate_limits)
        absolute_limits = self._build_absolute_limits(absolute_limits)
        output = {'limits': {'rate': rate_limits, 
                      'absolute': absolute_limits}}
        return output

    def _build_absolute_limits(self, absolute_limits):
        """Builder for absolute limits

        absolute_limits should be given as a dict of limits.
        For example: {"ram": 512, "gigabytes": 1024}.

        """
        limit_names = {'ram': [
                 'maxTotalRAMSize'], 
           'instances': [
                       'maxTotalInstances'], 
           'cores': [
                   'maxTotalCores'], 
           'gigabytes': [
                       'maxTotalHardwareGigabytes'], 
           'storages': [
                      'maxTotalHardwares'], 
           'key_pairs': [
                       'maxTotalKeypairs'], 
           'floating_ips': [
                          'maxTotalFloatingIps'], 
           'metadata_items': [
                            'maxServerMeta', 'maxImageMeta'], 
           'injected_files': [
                            'maxPersonality'], 
           'injected_file_content_bytes': [
                                         'maxPersonalitySize']}
        limits = {}
        for name, value in absolute_limits.iteritems():
            if name in limit_names and value is not None:
                for name in limit_names[name]:
                    limits[name] = value

        return limits

    def _build_rate_limits(self, rate_limits):
        limits = []
        for rate_limit in rate_limits:
            _rate_limit_key = None
            _rate_limit = self._build_rate_limit(rate_limit)
            for limit in limits:
                if limit['uri'] == rate_limit['URI'] and limit['regex'] == rate_limit['regex']:
                    _rate_limit_key = limit
                    break

            if not _rate_limit_key:
                _rate_limit_key = {'uri': rate_limit['URI'], 'regex': rate_limit['regex'], 
                   'limit': []}
                limits.append(_rate_limit_key)
            _rate_limit_key['limit'].append(_rate_limit)

        return limits

    def _build_rate_limit(self, rate_limit):
        _get_utc = datetime.datetime.utcfromtimestamp
        next_avail = _get_utc(rate_limit['resetTime'])
        return {'verb': rate_limit['verb'], 
           'value': rate_limit['value'], 
           'remaining': int(rate_limit['remaining']), 
           'unit': rate_limit['unit'], 
           'next-available': timeutils.isotime(at=next_avail)}