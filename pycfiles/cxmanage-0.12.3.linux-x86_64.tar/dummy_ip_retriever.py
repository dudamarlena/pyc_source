# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy_ip_retriever.py
# Compiled at: 2017-02-08 04:42:30
""" Dummy implementation of cxmanage_api.ipretriever.IPRetriever """
from cxmanage_api.cx_exceptions import IPDiscoveryError

class DummyIPRetriever(object):
    """ Dummy IP retriever """

    def __init__(self, ecme_ip, aggressive=False, verbosity=0, **kwargs):
        self.executed = False
        self.ecme_ip = ecme_ip
        self.aggressive = aggressive
        self.verbosity = verbosity
        self.server_ip = None
        for name, value in kwargs.iteritems():
            setattr(self, name, value)

        return

    def run(self):
        """ Set the server_ip variable. Raises an error if called more than
        once. """
        if self.executed:
            raise IPDiscoveryError('DummyIPRetriever.run() was called twice!')
        self.executed = True
        self.server_ip = '192.168.200.1'