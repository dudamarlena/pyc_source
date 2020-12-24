# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/scheduler/filters/capabilities_filter.py
# Compiled at: 2016-06-13 14:11:03
from vsm.openstack.common import log as logging
from vsm.openstack.common.scheduler import filters
from vsm.openstack.common.scheduler.filters import extra_specs_ops
LOG = logging.getLogger(__name__)

class CapabilitiesFilter(filters.BaseHostFilter):
    """HostFilter to work with resource (instance & storage) type records."""

    def _satisfies_extra_specs(self, capabilities, resource_type):
        """Check that the capabilities provided by the services
        satisfy the extra specs associated with the instance type"""
        extra_specs = resource_type.get('extra_specs', [])
        if not extra_specs:
            return True
        else:
            for key, req in extra_specs.iteritems():
                scope = key.split(':')
                if len(scope) > 1 and scope[0] != 'capabilities':
                    continue
                else:
                    if scope[0] == 'capabilities':
                        del scope[0]
                    cap = capabilities
                    for index in range(0, len(scope)):
                        try:
                            cap = cap.get(scope[index], None)
                        except AttributeError:
                            return False

                        if cap is None:
                            return False

                    if not extra_specs_ops.match(cap, req):
                        return False

            return True

    def host_passes(self, host_state, filter_properties):
        """Return a list of hosts that can create instance_type."""
        resource_type = filter_properties.get('resource_type')
        if not self._satisfies_extra_specs(host_state.capabilities, resource_type):
            return False
        return True