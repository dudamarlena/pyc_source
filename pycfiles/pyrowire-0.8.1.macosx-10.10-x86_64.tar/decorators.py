# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/decorators/decorators.py
# Compiled at: 2014-11-25 17:55:10
import pyrowire.config as config

def handler(topic=None):
    """
    decorator function that adds a processor to its topic in the application config
    :param topic: name of the topic to which to add the function
    :return: function, add_processor
    """

    def add_processor(f):
        config.add_handler(topic, f)

    return add_processor


def validator(name=None):
    """
    decorator function that adds a filter to the application's filter set
    :param name: name of the filter (should match the function name)
    :return: function, add_filter
    """

    def add_filter(f):
        filter_name = name or f.__name__
        config.add_validator(f)

    return add_filter