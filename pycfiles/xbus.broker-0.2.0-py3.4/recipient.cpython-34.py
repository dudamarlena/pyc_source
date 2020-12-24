# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/core/back/recipient.py
# Compiled at: 2016-06-27 03:37:50
# Size of source mod 2**32: 2502 bytes
import asyncio, aiozmq, logging
from xbus.broker.core.features import RecipientFeature
log = logging.getLogger(__name__)

class Recipient(object):
    __doc__ = 'Information about an Xbus recipient (a worker or a consumer):\n    - its metadata;\n    - the features it supports;\n    - a socket.\n    '

    def __init__(self, token, role_id):
        self.token = token
        self.role_id = role_id
        self.features = {}
        self.socket = None
        self.metadata = None

    def connect(self, url):
        """Initialize the recipient information holder. Open a socket to the
        specified URL and use it to fetch metadata and supported features.

        :param url: URL to reach the recipient.
        """
        log.info('Connecting to the recipient at %s' % url)
        self.socket = yield from aiozmq.rpc.connect_rpc(connect=url)
        log.info('Getting metadata from the recipient at %s' % url)
        self.metadata = yield from self.socket.call.get_metadata()
        log.info('Getting features from the recipient at %s' % url)
        yield from self.update_features()

    @asyncio.coroutine
    def ping(self) -> bool:
        yield from self.socket.call.ping(self.token)
        return self

    def has_feature(self, feature: RecipientFeature):
        """Tell whether the recipient has declared support for the specified
        feature.

        :param feature: Feature to check for.
        """
        return feature.name in self.features

    def update_features(self):
        """Refresh the list of features the recipient supports.
        :note: The socket must be open.
        """
        self.features = {}
        for feature in RecipientFeature:
            self.features[feature.name] = [
             False]
            feature_data = yield from getattr(self.socket.call, 'has_%s' % feature.name)()
            if not not feature_data:
                if not isinstance(feature_data, (list, tuple)):
                    continue
                if not feature_data[0]:
                    continue
                self.features[feature.name] = feature_data