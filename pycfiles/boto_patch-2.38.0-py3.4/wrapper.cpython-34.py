# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/beanstalk/wrapper.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1078 bytes
"""Wraps layer1 api methods and converts layer1 dict responses to objects."""
from boto.beanstalk.layer1 import Layer1
import boto.beanstalk.response
from boto.exception import BotoServerError
import boto.beanstalk.exception as exception

def beanstalk_wrapper(func, name):

    def _wrapped_low_level_api(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except BotoServerError as e:
            raise exception.simple(e)

        cls_name = ''.join([part.capitalize() for part in name.split('_')]) + 'Response'
        cls = getattr(boto.beanstalk.response, cls_name)
        return cls(response)

    return _wrapped_low_level_api


class Layer1Wrapper(object):

    def __init__(self, *args, **kwargs):
        self.api = Layer1(*args, **kwargs)

    def __getattr__(self, name):
        try:
            return beanstalk_wrapper(getattr(self.api, name), name)
        except AttributeError:
            raise AttributeError('%s has no attribute %r' % (self, name))