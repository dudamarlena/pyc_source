# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/capability_stub.py
# Compiled at: 2010-12-12 04:36:57
"""TyphoonAE's stub of the capability service API."""
import google.appengine.api.apiproxy_stub, google.appengine.api.capabilities
IsEnabledRequest = google.appengine.api.capabilities.IsEnabledRequest
IsEnabledResponse = google.appengine.api.capabilities.IsEnabledResponse
CapabilityConfig = google.appengine.api.capabilities.CapabilityConfig

class CapabilityServiceStub(google.appengine.api.apiproxy_stub.APIProxyStub):
    """Capability service stub."""

    def __init__(self, service_name='capability_service'):
        """Constructor.

        Args:
            service_name: Service name expected for all calls.
        """
        super(CapabilityServiceStub, self).__init__(service_name)

    def _Dynamic_IsEnabled(self, request, response):
        """Implementation of CapabilityService::IsEnabled().

        Args:
            request: An IsEnabledRequest.
            response: An IsEnabledResponse.
        """
        response.set_summary_status(IsEnabledResponse.ENABLED)
        default_config = response.add_config()
        default_config.set_package('')
        default_config.set_capability('')
        default_config.set_status(CapabilityConfig.ENABLED)