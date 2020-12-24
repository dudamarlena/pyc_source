# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/packagetrack/fedex.py
# Compiled at: 2010-07-14 13:16:41


class FedexInterface(object):

    def identify(self, tracking_number):
        return len(tracking_number) in (12, 15)

    def track(self, tracking_number):
        raise NotImplementedError

    def url(self, tracking_number):
        return 'http://www.fedex.com/Tracking?tracknumbers=%s' % tracking_number