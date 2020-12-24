# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: autoant/providers.py
# Compiled at: 2014-09-23 18:30:06


class Provider(object):
    """
        Class that keeps all classes from producers and processors
        map's them to config key.
    """

    def __init__(self):
        self._providers = list()

    def add(self, provider_type, key, provider_class, short_description):
        provider = dict()
        provider['key'] = key
        provider['provider_type'] = provider_type
        provider['class'] = provider_class
        provider['short_description'] = short_description
        self._providers.append(provider)

    def get_class(self, key):
        """
            Get class from key
        """
        for provider in self._providers:
            if provider['key'] == key:
                return provider['class']

    def get_short_description(self, cls):
        """
            Get short description from class
        """
        for provider in self._providers:
            if cls.__name__ == provider['class'].__name__:
                return provider['short_description']

    def __repr__(self):
        retstr = ''
        for provider in self._providers:
            retstr = retstr + ('{0}: key:{1} - {2}\n').format(provider['provider_type'], provider['key'], provider['short_description'])

        return retstr


providers = Provider()

def register_producer(key, short_description):

    def inner(cls):
        providers.add('Producer', key, cls, short_description)
        return cls

    return inner


def register_processor(key, short_description):

    def inner(cls):
        providers.add('Processor', key, cls, short_description)
        return cls

    return inner