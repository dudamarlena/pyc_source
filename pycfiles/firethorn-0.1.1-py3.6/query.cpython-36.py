# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/models/query.py
# Compiled at: 2019-02-10 20:18:00
# Size of source mod 2**32: 2991 bytes
"""
Created on Nov 4, 2017

@author: stelios
"""
import logging
from table import Table
from adql import adql_schema
try:
    import simplejson as json
except ImportError:
    import json

class Query(object):
    __doc__ = '\n    Query Class, stores information for a Firethorn query \n    \n    Attributes\n    ----------\n    querystring: string, optional\n        The Query as a sring\n\n    adql_resource: string, optional\n        The query Resource\n    \n    adql_query: string, optional\n        The AdqlQuery object\n        \n    account: Account, optional\n        Reference to the he Authentication Engine being used\n                  \n    '

    def __init__(self, querystring=None, adql_query=None, mode='SYNC'):
        self.adql_query = adql_query
        self.mode = mode
        self.querystring = querystring
        if self.adql_query != None:
            self.account = self.adql_query.account
        if mode == 'SYNC':
            self.run()

    @property
    def querystring(self):
        return self._Query__querystring

    @querystring.setter
    def querystring(self, querystring):
        self._Query__querystring = querystring

    @property
    def mode(self):
        return self._Query__mode

    @mode.setter
    def mode(self, mode):
        self._Query__mode = mode

    def run(self):
        """
        Run a query
        
        """
        try:
            if self.mode.upper() == 'SYNC':
                self.adql_query.run_sync()
            else:
                self.adql_query.update(adql_query_status_next='COMPLETED')
        except Exception as e:
            logging.exception(e)

    def update(self, query_input):
        """
        Run Query
        """
        try:
            self.adql_query.update(adql_query_input=query_input)
            self.querystring = query_input
        except Exception as e:
            logging.exception(e)

    def results(self):
        """
        Get Results
        
        """
        if self.adql_query != None:
            if self.adql_query.table() != None:
                return Table(adql_table=(self.adql_query.table()))

    def status(self):
        """
        Get Status 
        """
        if self.adql_query != None:
            return self.adql_query.status()

    def error(self):
        """
        Get Error message
        """
        if self.adql_query != None:
            return self.adql_query.error()

    def isRunning(self):
        """
        Check if a Query is running
        """
        if self.adql_query != None:
            return self.adql_query.isRunning()

    def __str__(self):
        """ Print class as string
        """
        return 'Query: %s\nQuery ID: %s\n ' % (self.querystring, self.adql_query.url)