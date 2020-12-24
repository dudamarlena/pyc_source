# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redlink/__init__.py
# Compiled at: 2015-11-07 08:35:34
"""
Redlink Python SDK: C{https://github.com/redlink-gmbh/redlink-python-sdk}
"""
__version__ = '1.0.1'
__authors__ = 'Sergio Fernandez'
__license__ = 'Apache License, Version 2.0'
__url__ = 'https://github.com/redlink-gmbh/redlink-python-sdk'
__contact__ = 'support@redlink.io'
__date__ = '2015-10-28'
__agent__ = 'RedlinkPythonSDK/%s' % __version__
from .analysis import RedlinkAnalysis
from .data import RedlinkData

def create_analysis_client(key):
    """
    Create an instance of a Redlink Analysis Client

    @type  key: str
    @param key: api key

    @rtype: C{RedlinkAnalysis}
    @return: analysis client
    """
    return RedlinkAnalysis(key)


def create_data_client(key):
    """
    Create an instance of a Redlink Dara Client

    @type  key: str
    @param key: api key

    @rtype: C{RedlinkData}
    @return: data client
    """
    return RedlinkData(key)