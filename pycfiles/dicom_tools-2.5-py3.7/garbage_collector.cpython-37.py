# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/util/garbage_collector.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1600 bytes
import gc
from ..Qt import QtCore

class GarbageCollector(object):
    __doc__ = '\n    Disable automatic garbage collection and instead collect manually\n    on a timer.\n\n    This is done to ensure that garbage collection only happens in the GUI\n    thread, as otherwise Qt can crash.\n\n    Credit:  Erik Janssens\n    Source:  http://pydev.blogspot.com/2014/03/should-python-garbage-collector-be.html\n    '

    def __init__(self, interval=1.0, debug=False):
        self.debug = debug
        if debug:
            gc.set_debug(gc.DEBUG_LEAK)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check)
        self.threshold = gc.get_threshold()
        gc.disable()
        self.timer.start(interval * 1000)

    def check(self):
        l0, l1, l2 = gc.get_count()
        if self.debug:
            print('gc_check called:', l0, l1, l2)
        if l0 > self.threshold[0]:
            num = gc.collect(0)
            if self.debug:
                print('collecting gen 0, found: %d unreachable' % num)
            if l1 > self.threshold[1]:
                num = gc.collect(1)
                if self.debug:
                    print('collecting gen 1, found: %d unreachable' % num)
                if l2 > self.threshold[2]:
                    num = gc.collect(2)
                    if self.debug:
                        print('collecting gen 2, found: %d unreachable' % num)

    def debug_cycles(self):
        gc.collect()
        for obj in gc.garbage:
            print(obj, repr(obj), type(obj))