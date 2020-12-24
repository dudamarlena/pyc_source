# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/customize25.py
# Compiled at: 2020-04-18 17:55:36
"""Isolate Python 2.5+ version-specific semantic actions here.
"""
from uncompyle6.semantics.consts import TABLE_DIRECT

def customize_for_version25(self, version):
    TABLE_DIRECT.update({'importmultiple': ('%|import %c%c\n', 2, 3), 'import_cont': (', %c', 2), 'with': ('%|with %c:\n%+%c%-', 0, 3), 'withasstmt': ('%|with %c as (%c):\n%+%c%-', 0, 2, 3)})

    def tryfinallystmt(node):
        if len(node[1][0]) == 1 and node[1][0][0] == 'stmt':
            if node[1][0][0][0] == 'try_except':
                node[1][0][0][0].kind = 'tf_try_except'
            if node[1][0][0][0] == 'tryelsestmt':
                node[1][0][0][0].kind = 'tf_tryelsestmt'
        self.default(node)

    self.n_tryfinallystmt = tryfinallystmt