# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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