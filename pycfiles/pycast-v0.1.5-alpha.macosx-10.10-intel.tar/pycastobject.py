# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/common/pycastobject.py
# Compiled at: 2015-05-28 05:27:44


class PyCastObject(object):
    """The base class for all pycast objects.

    This class is used to introduce a common interface for potential
    C/C++/OpenCL optimization within pycast, as well as other common
    tasks.
    """
    _globalOptimize = False

    def __init__(self):
        """Initializes the PyCastObject."""
        super(PyCastObject, self).__init__()
        self.optimizationEnabled = False
        if PyCastObject._globalOptimize:
            self._enable_instance_optimization()

    def _enable_instance_optimization(self):
        """Enables the optimization for the PyCastObject instance.

        :warning:    Do not forget to implement the disable_instance_optimization()
            as well.
        """
        self.optimizationEnabled = True

    def _disable_instance_optimization(self):
        """Disables the optimization for the PyCastObject instance.
        """
        self.optimizationEnabled = False

    @classmethod
    def enable_global_optimization(cls):
        """Enables the global optimization of pycast methods, if possible.

        By default, optimization is turned off.

        :note:    Only new created instances will be affected.
        """
        cls._globalOptimize = True

    @classmethod
    def disable_global_optimization(cls):
        """Disables the global optimization of pycast methods.

        :note:    Only new created instances will be affected.
        """
        cls._globalOptimize = False