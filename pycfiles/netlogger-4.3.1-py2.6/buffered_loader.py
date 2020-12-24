# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/modules/buffered_loader.py
# Compiled at: 2010-05-06 18:48:58
"""
Tester/example module showing use of the threaded BufferedAnalyzer
class.  Works in much the same fashion as the normal Analyzer class
but the user overrides the process_buffer() method rather than the 
process() method.  Other than that, a dict-i-fied version of a line
from a BP log is passed in and the user processes it as they will.
"""
__rcsid__ = '$Id$'
__author__ = 'Monte Goode'
from netlogger.analysis.modules._base import BufferedAnalyzer as BaseAnalyzer
import time

class Analyzer(BaseAnalyzer):
    """Test module for BufferedAnalyzer.
    """

    def __init__(self):
        """Ctor
        """
        BaseAnalyzer.__init__(self)

    def process_buffer(self, row):
        """Do 'something' with input row and introduce
        a lag for testing purposes.
        """
        self.log.debug('process_buffer', msg=row)
        time.sleep(0.1)