# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/inline/pragma.py
# Compiled at: 2018-11-21 11:13:57
# Size of source mod 2**32: 2438 bytes


class Pragma(object):
    """Pragma"""
    priority = 25

    def match(self, context, line):
        """Match "pragma" command usage."""
        return line.kind == 'code' and line.stripped.startswith('pragma ')

    def __call__(self, context):
        flags = [i.lower().strip() for i in context.input.next().stripped.split()][1:]
        for flag in flags:
            if not flag.strip('!'):
                continue
            if flag[0] == '!':
                flag = flag[1:]
                if flag in context.flag:
                    context.flag.remove(flag)
                    continue
                if flag not in context.flag:
                    context.flag.add(flag)

        if False:
            yield None