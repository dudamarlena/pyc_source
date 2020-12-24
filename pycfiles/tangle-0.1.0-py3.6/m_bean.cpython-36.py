# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/tangle/m_bean.py
# Compiled at: 2017-08-24 10:01:45
# Size of source mod 2**32: 1140 bytes
import six

class _Field(property):

    def __init__(self, klass, autowire, *args, **kwargs):
        (super(_Field, self).__init__)(*args, **kwargs)
        self.klass = klass
        self.autowire = autowire


class Field(object):

    def __init__(self, klass, autowire=False):
        super(Field, self).__init__()
        self.klass = klass
        self.autowire = autowire

    def register(self, fn):
        pass

    def __call__(self, fn):
        self.register(fn)

        def _getter(inst):
            try:
                return getattr(inst, '_' + fn.__name__)
            except AttributeError:
                six.raise_from(AttributeError('property (%s) not set yet!' % fn.__name__), None)

        def _setter(inst, value):
            if not isinstance(value, self.klass):
                raise TypeError('set property type (%s) wrong!' % self.klass.__name__)
            setattr(inst, '_' + fn.__name__, value)

        return _Field(self.klass, self.autowire, _getter, _setter)