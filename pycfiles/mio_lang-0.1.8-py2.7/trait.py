# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/trait.py
# Compiled at: 2013-12-08 17:19:04
from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import TypeError

class Trait(Object):

    def __init__(self):
        super(Trait, self).__init__()
        self.requirements = []
        self.create_methods()
        self.parent = runtime.find('Trait' if self.__class__ is not Trait else 'Object')

    def __setitem__(self, key, value):
        if getattr(value, 'type', None) != 'Block':
            raise TypeError('Traits cannot contain state!')
        super(Trait, self).__setitem__(key, value)
        return

    @method()
    def init(self, receiver, context, m):
        receiver.requirements = []
        return receiver

    @method()
    def requires(self, receiver, context, m, *methods):
        receiver.requirements.extend(list(runtime.state.frommio(method.eval(context)) for method in methods))
        return receiver

    @method()
    def requirements(self, receiver, context, m):
        return runtime.state.tomio(receiver.requirements)