# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/customize26_27.py
# Compiled at: 2020-01-14 12:41:01
"""Isolate Python 2.6 and 2.7 version-specific semantic actions here.
"""
from uncompyle6.semantics.consts import TABLE_DIRECT

def customize_for_version26_27(self, version):
    if version > 2.6:
        TABLE_DIRECT.update({'except_cond2': ('%|except %c as %c:\n', 1, 5), 'call_generator': ('%c%P', 0, (1, -1, ', ', 100))})
    else:
        TABLE_DIRECT.update({'testtrue_then': ('not %p', (0, 22))})

    def n_call(node):
        mapping = self._get_mapping(node)
        key = node
        for i in mapping[1:]:
            key = key[i]

        if key.kind == 'CALL_FUNCTION_1':
            args_node = node[(-2)]
            if args_node == 'expr':
                n = args_node[0]
                if n == 'generator_exp':
                    node.kind = 'call_generator'
        self.default(node)

    self.n_call = n_call