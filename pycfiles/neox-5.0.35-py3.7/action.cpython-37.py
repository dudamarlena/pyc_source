# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/action.py
# Compiled at: 2019-03-03 16:06:11
# Size of source mod 2**32: 1186 bytes
import os, tempfile
from neox.commons.common import slugify, file_open
from neox.commons.rpc import RPCProgress

class Action(object):

    @staticmethod
    def exec_report(conn, name, data, direct_print=False, context=None):
        if context is None:
            context = {}
        data = data.copy()
        ctx = {}
        ctx.update(context)
        ctx['direct_print'] = direct_print
        args = ('report', name, 'execute', data.get('ids', []), data, ctx)
        try:
            rpc_progress = RPCProgress(conn, 'execute', args)
            res = rpc_progress.run()
        except:
            return False
            if not res:
                return False
            type, content, print_p, name = res
            dtemp = tempfile.mkdtemp(prefix='tryton_')
            fp_name = os.path.join(dtemp, slugify(name) + os.extsep + slugify(type))
            print(dtemp)
            if os.name == 'nt':
                operation = 'open'
                os.startfile(fp_name, operation)
            else:
                with open(fp_name, 'wb') as (file_d):
                    file_d.write(content.data)
                file_open(fp_name, type, direct_print=direct_print)
            return True