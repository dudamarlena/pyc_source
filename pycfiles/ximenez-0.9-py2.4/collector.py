# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/collectors/collector.py
# Compiled at: 2007-11-10 08:06:38
"""Define ``Collector`` abstract class.

$Id: collector.py 8 2007-11-10 13:06:44Z damien.baty $
"""
from ximenez.input import InputAware

class Collector(object, InputAware):
    """The purpose of a collector is to collect information.

    ``Collector`` is an abstract class which real collector plug-ins
    must subclass.
    """
    __module__ = __name__

    def collect(self):
        """Collect informations and return a tuple of items (the type
        of these items depends on the purpose of this collector).

        This method **must** be implemented.
        """
        raise NotImplementedError