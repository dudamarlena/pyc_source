# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/util/deprecation.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1581 bytes
import warnings
warnings.filterwarnings('always', category=DeprecationWarning, module='locust')

def check_for_deprecated_wait_api(locust_or_taskset):
    if locust_or_taskset.wait_function:
        warnings.warn('Usage of wait_function is deprecated since version 0.13. Declare a %s.wait_time method instead (should return seconds and not milliseconds)' % type(locust_or_taskset).__name__, DeprecationWarning)
        from locust.core import TaskSet
        if not locust_or_taskset.wait_time or locust_or_taskset.wait_time.__func__ == TaskSet.wait_time:
            locust_or_taskset.wait_time = lambda : locust_or_taskset.wait_function() / 1000.0
    if locust_or_taskset.min_wait is not None:
        if locust_or_taskset.max_wait is not None:

            def format_min_max_wait(i):
                float_value = i / 1000.0
                if float_value == int(float_value):
                    return '%i' % int(float_value)
                return '%.3f' % float_value

            warnings.warn('Usage of min_wait and max_wait is deprecated since version 0.13. Instead use: wait_time = between(%s, %s)' % (
             format_min_max_wait(locust_or_taskset.min_wait),
             format_min_max_wait(locust_or_taskset.max_wait)), DeprecationWarning)