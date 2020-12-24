# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/traits/cloneable.py
# Compiled at: 2013-12-03 08:27:17
from mio import runtime
from mio.trait import Trait
from mio.utils import method

class TCloneable(Trait):

    @method()
    def clone(self, receiver, context, m, *args):
        obj = receiver.clone()
        m = runtime.find('Message').clone()
        m.name = 'init'
        m.args = args
        m.call = True
        m.eval(obj, context, m)
        return obj