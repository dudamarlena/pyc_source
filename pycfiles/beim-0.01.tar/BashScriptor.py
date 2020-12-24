# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/envvars/renderers/BashScriptor.py
# Compiled at: 2013-12-08 21:45:16


class BashScriptor(object):

    def render(self, operations):
        self._lines = []
        for op in operations:
            self._lines += op.identify(self)
            continue

        return self._lines

    def onSet(self, op):
        return [
         'export %s="%s"' % (op.name, op.value)]

    def onAppend(self, op):
        return [
         'export %s=$%s:"%s"' % (op.name, op.name, op.value)]

    def onPrepend(self, op):
        return [
         'export %s="%s":$%s' % (op.name, op.value, op.name)]