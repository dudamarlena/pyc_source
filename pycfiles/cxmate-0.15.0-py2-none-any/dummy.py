# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = ' Module for the generic Dummy class '
from mock import Mock

class Dummy(Mock):
    """ Dummy class. Children of this class will automatically have their
    methods be turned into Mock objects with side effects, allowing us to track
    their usage and assert about how they are called.

    They dummy_spec variable gives us a spec for building the Mock object, which
    restricts the names of methods that can be called.

    """
    dummy_spec = None

    def __init__(self):
        super(Dummy, self).__init__(spec=self.dummy_spec)
        for name in dir(self):
            if not hasattr(Mock, name):
                try:
                    attr = getattr(self, name)
                    if callable(attr) and not isinstance(attr, Mock):
                        setattr(self, name, Mock(side_effect=attr))
                except AttributeError:
                    pass

    def _get_child_mock(self, *args, **kwargs):
        return Mock(*args, **kwargs)