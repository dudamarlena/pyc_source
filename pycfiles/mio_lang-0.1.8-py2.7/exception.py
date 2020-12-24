# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/core/exception.py
# Compiled at: 2013-12-08 17:19:04
from sys import exc_info
from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import UserError

class Exception(Object):

    @method('try')
    def tryEval(self, receiver, context, m, code):
        try:
            return code.eval(context)
        except:
            etype, evalue, _ = exc_info()
            error = etype.__name__
            message = str(evalue)
            return runtime.state.eval(('Error primitive("clone") init("{0:s}", "{1:s}")').format(error, message))

    @method('raise')
    def raiseError(self, receiver, context, m, error):
        raise UserError(error.eval(context))