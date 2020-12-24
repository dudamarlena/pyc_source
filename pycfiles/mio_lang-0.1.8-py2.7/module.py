# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/core/module.py
# Compiled at: 2013-12-08 17:19:04
from mio import runtime
from mio.parser import parse
from mio.utils import method
from mio.object import Object
from mio.lexer import tokenize

class Module(Object):

    def __init__(self):
        super(Module, self).__init__()
        self.file = None
        self.name = None
        self.create_methods()
        self.parent = runtime.find('Object')
        return

    def __repr__(self):
        return ('Module(name={0:s}, file={1:s})').format(repr(self.name), repr(self.file))

    @method()
    def init(self, receiver, context, m, name, file):
        receiver.name = name = str(name)
        receiver.file = file = str(file)
        runtime.state.load(file, receiver, receiver)
        return receiver

    @method('import')
    def _import(self, receiver, context, m, name):
        name = name.name if name.value is None else unicode(name.eval(context))
        if context.type == 'Module' and receiver is context:
            m = parse(tokenize(('Importer import("{0:s}")').format(name)))
            return m.eval(receiver, context, m)
        else:
            if name == '*':
                context.attrs.update(receiver.attrs)
            else:
                context[name] = receiver[name]
            return runtime.find('None')