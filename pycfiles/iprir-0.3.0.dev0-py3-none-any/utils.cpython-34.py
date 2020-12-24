# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib/iprir/utils.py
# Compiled at: 2017-03-21 22:23:05
# Size of source mod 2**32: 718 bytes
_logger = None

def set_logger(logger):
    global _logger
    _logger = logger


def get_logger():
    return _logger


class cached_property:
    __doc__ = '\n    Descriptor (non-data) for building an attribute on-demand on first use.\n\n    ref: http://stackoverflow.com/a/4037979/3886899\n    '
    __slots__ = ('_factory', )

    def __init__(self, factory):
        """
        <factory> is called such: factory(instance) to build the attribute.
        """
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._factory.__name__, attr)
        return attr