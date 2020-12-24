# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wirecloud_pubsub/wirecloud.py
# Compiled at: 2012-02-16 19:24:00
from ezweb.plugins import WirecloudPlugin
from wirecloud_pubsub import VERSION

class PubSubPlugin(WirecloudPlugin):
    features = {'PubSub': ('.').join(map(str, VERSION))}

    def get_scripts(self, view):
        return ('js/lib/silbops/events.js', 'js/lib/silbops/endpoint.js', 'js/lib/silbops/pubendpoint.js',
                'js/lib/silbops/subendpoint.js', 'js/lib/silbops/stream.js', 'js/lib/silbops/silbops.js',
                'js/lib/silbops/eventsource.js', 'js/lib/silbops/filter.js', 'js/pubsub/PubSubManager.js')

    def get_gadget_api_extensions(self, view):
        return ('js/EzWebAPI/PubSub.js', )