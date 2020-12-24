# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/scheduler/filters/availability_zone_filter.py
# Compiled at: 2016-06-13 14:11:03
from vsm.openstack.common.scheduler import filters

class AvailabilityZoneFilter(filters.BaseHostFilter):
    """Filters Hosts by availability zone."""

    def host_passes(self, host_state, filter_properties):
        spec = filter_properties.get('request_spec', {})
        props = spec.get('resource_properties', [])
        availability_zone = props.get('availability_zone')
        if availability_zone:
            return availability_zone == host_state.service['availability_zone']
        return True