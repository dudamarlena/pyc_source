# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/speck/expectation.py
# Compiled at: 2012-05-30 18:21:13
from functools import partial
from .matcher import matchers

class _(object):

    def __init__(self, value):
        self.__speck_value = value

    @property
    def should(self):
        return Should(self.__speck_value)

    @property
    def should_not(self):
        return Should(self.__speck_value, negated=True)


class Expectation(object):

    def __init__(self, value, negated=False):
        self.value = value
        self.negated = negated

    def __getattr__(self, name):
        if name.startswith('not_'):
            return getattr(type(self)(self.value, not self.negated), name[4:])
        return self.matcher(name)

    def matcher(self, name):
        return partial(matchers.get(name, negated=self.negated), self.value)

    __eq__ = lambda s, o: s.matcher('==')(o)
    __ne__ = lambda s, o: s.matcher('!=')(o)
    __lt__ = lambda s, o: s.matcher('<')(o)
    __le__ = lambda s, o: s.matcher('<=')(o)
    __gt__ = lambda s, o: s.matcher('>')(o)
    __ge__ = lambda s, o: s.matcher('>=')(o)


class Should(Expectation):

    def __getattr__(self, name):
        if name.startswith('be_'):
            return getattr(self.be, name[3:])
        return super(Should, self).__getattr__(name)

    @property
    def be(self):
        return Be(self.value, self.negated)


class Be(Expectation):

    def __call__(self, other):
        return self.matcher('is')(other)

    def __nonzero__(self):
        return self.matcher('true')(self)