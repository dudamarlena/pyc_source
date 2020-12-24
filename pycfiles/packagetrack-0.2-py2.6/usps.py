# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/packagetrack/usps.py
# Compiled at: 2010-06-21 16:10:10


class USPSInterface(object):

    def identify(self, tracking_number):
        return tracking_number.startswith('91')

    def url(self, tracking_number):
        return 'http://trkcnfrm1.smi.usps.com/PTSInternetWeb/InterLabelInquiry.do?origTrackNum=%s' % tracking_number