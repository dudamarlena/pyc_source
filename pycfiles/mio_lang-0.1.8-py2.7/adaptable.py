# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/traits/adaptable.py
# Compiled at: 2013-12-08 17:19:04
from mio import runtime
from mio.trait import Trait
from mio.utils import method
from mio.errors import TypeError

class TAdaptable(Trait):

    def __init__(self):
        super(TAdaptable, self).__init__()
        Object = runtime.find('Object')
        Object.__addtrait__(self)

    @method()
    def use(self, receiver, context, m, trait, resolution=None):
        trait = trait.eval(context)
        if receiver.__hastrait__(trait):
            raise TypeError(('{0:s} already uses {1:s}').format(repr(receiver), repr(trait)))
        resolution = runtime.state.frommio(resolution.eval(context)) if resolution is not None else {}
        receiver.__addtrait__(trait, **resolution)
        return receiver

    @method()
    def delTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        if not receiver.__hastrait__(trait):
            raise TypeError(('{0:s} does not use {1:s}').format(repr(receiver), repr(trait)))
        receiver.__deltrait__(trait)
        return receiver

    @method()
    def hasTrait(self, receiver, context, m, trait):
        trait = trait.eval(context)
        if receiver.__hastrait__(trait):
            return runtime.find('True')
        return runtime.find('False')

    @method('traits', True)
    def getTraits(self, receiver, context, m):
        return runtime.find('List').clone(receiver.traits.keys())

    @method('behaviors', True)
    def getBehaviors(self, receiver, context, m):
        return runtime.find('List').clone(receiver.behaviors.keys())

    @method()
    def adapt(self, receiver, context, m, trait):
        trait = trait.eval(context)
        obj = receiver.clone()
        obj.__addtrait__(trait)
        return obj