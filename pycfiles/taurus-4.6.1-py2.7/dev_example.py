# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/evaluation/test/res/dev_example.py
# Compiled at: 2019-08-19 15:09:29
"""
Examples on using the evaluation scheme for exposing arbitrary non-tango quantities as taurus attributes
"""
from __future__ import print_function
import os, platform, ctypes
from taurus.core.evaluation import EvaluationDevice
from taurus.core.units import Quantity
__all__ = [
 'FreeSpaceDevice']

class FreeSpaceDevice(EvaluationDevice):
    """A simple example of usage of the evaluation scheme for
    creating a device that allows to obtain available space in a dir.

    Important: note that only those members listed in `_symbols` will be available
    """
    _symbols = [
     'getFreeSpace']
    _x = 1

    def getFreeSpace(self, dir):
        """ return free space (in bytes).
        (Recipe adapted from `http://stackoverflow.com/questions/51658`)
        """
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir), None, None, ctypes.pointer(free_bytes))
            ret = free_bytes.value
        else:
            s = os.statvfs(dir)
            ret = s.f_bsize * s.f_bavail
        return Quantity(ret, 'B')


def test1():
    import taurus
    a = taurus.Attribute('eval:@taurus.core.evaluation.test.res.dev_example.FreeSpaceDevice/getFreeSpace("/").to("GiB")')
    print(('Free space: {:s}').format(a.read().rvalue), a.read().rvalue.units)


def test2():
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    from taurus.qt.qtgui.panel import TaurusForm
    app = TaurusApplication(cmd_line_parser=None)
    w = TaurusForm()
    attrname = 'eval:@taurus.core.evaluation.test.res.dev_example.FreeSpaceDevice/getFreeSpace("/")'
    w.setModel(attrname)
    w.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    test1()
    test2()