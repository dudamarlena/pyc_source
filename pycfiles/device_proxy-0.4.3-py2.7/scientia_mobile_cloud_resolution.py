# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devproxy/handlers/wurfl_handler/scientia_mobile_cloud_resolution.py
# Compiled at: 2014-07-28 10:42:31
from devproxy.handlers.wurfl_handler.scientia_mobile_cloud import ScientiaMobileCloudHandler

class ScientiaMobileCloudResolutionHandler(ScientiaMobileCloudHandler):
    """The initial implementation. This remains as legacy. Use of
    ScientiaMobileCloudResolutionTouchHandler is recommended."""

    def handle_device(self, request, device):
        if device['capabilities']['resolution_width'] > 240:
            return [{self.header_name: 'high'}]
        else:
            return [{self.header_name: 'medium'}]


class ScientiaMobileCloudResolutionTestHandler(ScientiaMobileCloudResolutionHandler):
    """Handler used in tests. Do not use in production."""

    def handle_user_agent(self, user_agent):
        if user_agent == 'Some special bot':
            return [{self.header_name: 'bot'}]
        else:
            return


class ScientiaMobileCloudResolutionTouchHandler(ScientiaMobileCloudHandler):

    def handle_device(self, request, device):
        result = {self.header_name: self.default_ua_map}
        is_web_browser = False
        is_smart_browser = False
        is_basic_browser = False
        try:
            is_web_browser = device['capabilities']['ux_full_desktop'] or device['capabilities']['is_tablet']
            is_smart_browser = device['capabilities']['resolution_width'] >= 320 and device['capabilities']['pointing_method'] == 'touchscreen'
            is_basic_browser = not (is_web_browser or is_smart_browser)
        except KeyError:
            pass

        if is_web_browser:
            result[self.header_name] = 'web'
        elif is_smart_browser:
            result[self.header_name] = 'smart'
        elif is_basic_browser:
            result[self.header_name] = 'basic'
        return [result]