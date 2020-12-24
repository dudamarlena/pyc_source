# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/mongopony/tests/base.py
# Compiled at: 2015-09-09 03:09:16
from pymongo import MongoClient
from .. import local_config

class ConnectionMixin(object):

    def setUp(self):
        self.client = MongoClient(local_config.host, local_config.port)
        super(ConnectionMixin, self).setUp()