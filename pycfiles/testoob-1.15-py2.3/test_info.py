# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/test_info.py
# Compiled at: 2009-10-07 18:08:46
"""getting information about tests"""

def create_test_info(arg):
    """
    Factory method for creating TestInfo instances.
    """
    if isinstance(arg, TestInfo):
        return arg
    return TestInfo(arg)


class TestInfo:
    """
    An interface for getting information about tests.
    Reporters receive instances of this class.
    """
    __module__ = __name__

    def __init__(self, fixture):
        self.fixture = fixture

    def module(self):
        return self.fixture.__module__

    def filename(self):
        import sys
        try:
            return sys.modules[self.module()].__file__
        except KeyError:
            return 'unknown file'

    def classname(self):
        return self.fixture.__class__.__name__

    def funcname(self):
        return self.fixture.id().split('.')[(-1)]

    def extrainfo(self):
        return self.fixture._testoob_extra_description

    def extrafuncname(self):
        return '%s%s' % (self.funcname(), self.extrainfo())

    def docstring(self):
        if getattr(self.fixture, self.funcname()).__doc__:
            return getattr(self.fixture, self.funcname()).__doc__.splitlines()[0]
        return ''

    def funcinfo(self):
        return (
         self.funcname(), self.docstring(), self.extrainfo())

    def failure_exception_type(self):
        return self.fixture.failureException

    def id(self):
        return self.fixture.id()

    def short_description(self):
        return self.fixture.shortDescription()

    def __str__(self):
        return str(self.fixture)

    def __unique_string_repr(self):
        return '%s - %s' % (hash(self), str(self))

    def __cmp__(self, other):
        try:
            return cmp(self.fixture, other.fixture)
        except AttributeError:
            return cmp(self.__unique_string_repr(), other.__unique_string_repr())

    def __hash__(self):
        return hash(self.fixture)


from testoob.utils import add_fields_pickling
add_fields_pickling(TestInfo)