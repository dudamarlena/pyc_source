# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/copy_access.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class CopyObjectACLs(Command):
    __domain__ = 'object'
    __operation__ = 'copy-access'

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        self._source = params.get('source', None)
        self._target = params.get('target', None)
        if self._source is None or self._target is None:
            raise CoilsException('Either source or target not provided to object::copy-access')
        return

    def run(self, **params):
        acls = self._ctx.run_command('object::get-access', object=self._source)
        if len(acls) > 0:
            for acl in acls:
                self._ctx.run_command('object::get-access', object=self._source)