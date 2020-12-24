# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/gazehound/readers/auto_pointpath.py
# Compiled at: 2010-07-20 17:32:44
from __future__ import with_statement
from gazehound.readers.iview import IView2ScanpathReader, IView3PointPathReader

class AutoPointpathReader(object):

    def __init__(self, try_order=[
 IView2ScanpathReader,
 IView3PointPathReader]):
        self.try_order = try_order
        self.failures = []
        self.success_class = None
        return

    def read_pointpath(self, filename=None, file_data=None):
        for klass in self.try_order:
            reader = klass(filename=filename, file_data=file_data)
            try:
                pp = reader.pointpath()
                if pp is not None:
                    self.success_class = klass
                    return pp
            except Exception, exc:
                self.failures.append((klass, exc))

        return