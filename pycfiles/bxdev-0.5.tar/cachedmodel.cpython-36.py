# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bxa/sherpa/cachedmodel.py
# Compiled at: 2020-01-28 12:31:59
# Size of source mod 2**32: 1968 bytes
from __future__ import print_function
import os, numpy
from math import log10, isnan, isinf
if 'MAKESPHINXDOC' not in os.environ:
    import sherpa.astro.ui as ui
    from sherpa.stats import Cash, CStat
    from sherpa.models import ArithmeticModel, CompositeModel
else:
    ArithmeticModel = object
    CompositeModel = list

class VariableCachedModel(CompositeModel, ArithmeticModel):

    def __init__(self, othermodel):
        self.othermodel = othermodel
        self.cache = None
        self.lastp = None
        print('calling CompositeModel...')
        CompositeModel.__init__(self, name=('cached(%s)' % othermodel.name), parts=(othermodel,))

    def calc(self, p, left, right, *args, **kwargs):
        if self.cache is None or self.lastp != p:
            self.cache = (self.othermodel.calc)(p, left, right, *args, **kwargs)
            self.lastp = p
        return self.cache

    def startup(self):
        self.othermodel.startup()
        CompositeModel.startup(self)

    def teardown(self):
        self.othermodel.teardown()
        CompositeModel.teardown(self)

    def guess(self, dep, *args, **kwargs):
        (self.othermodel.guess)(dep, *args, **kwargs)
        (CompositeModel.guess)(self, dep, *args, **kwargs)


class CachedModel(CompositeModel, ArithmeticModel):

    def __init__(self, othermodel):
        self.othermodel = othermodel
        self.cache = None
        CompositeModel.__init__(self, name=('cached(%s)' % othermodel.name), parts=(othermodel,))

    def calc(self, *args, **kwargs):
        if self.cache is None:
            print('   computing cached model ... ')
            self.cache = (self.othermodel.calc)(*args, **kwargs)
        return self.cache

    def startup(self):
        self.othermodel.startup()
        CompositeModel.startup(self)

    def teardown(self):
        self.othermodel.teardown()
        CompositeModel.teardown(self)

    def guess(self, dep, *args, **kwargs):
        (self.othermodel.guess)(dep, *args, **kwargs)
        (CompositeModel.guess)(self, dep, *args, **kwargs)