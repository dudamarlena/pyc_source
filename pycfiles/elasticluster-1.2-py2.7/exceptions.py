# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/elasticluster/exceptions.py
# Compiled at: 2014-10-22 16:00:16
__author__ = 'Nicolas Baer <nicolas.baer@uzh.ch>'

class ConfigurationError(Exception):
    pass


class SecurityGroupError(Exception):
    pass


class KeypairError(Exception):
    pass


class InstanceError(Exception):
    pass


class FlavorError(Exception):
    pass


class TimeoutError(Exception):
    pass


class ClusterNotFound(Exception):
    pass


class ClusterError(Exception):
    pass


class NodeNotFound(Exception):
    pass


class ImageError(Exception):
    pass


class CloudProviderError(Exception):
    pass