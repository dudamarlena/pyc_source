# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/tools/inside_reaper.py
# Compiled at: 2019-02-23 10:10:45
# Size of source mod 2**32: 822 bytes
import reapy
if not reapy.is_inside_reaper():
    from . import dist_program

class InsideReaper:
    __doc__ = '\n    Context manager for efficient calls from outside REAPER.\n\n    Examples\n    --------\n    Instead of running:\n\n    >>> project = reapy.Project()\n    >>> l = [project.bpm for i in range(1000)\n\n    which takes around 30 seconds, run:\n\n    >>> project = reapy.Project()\n    >>> with reapy.inside_reaper():\n    ...     l = [project.bpm for i in range(1000)\n    ...\n\n    which takes 0.1 seconds!\n    '

    def __enter__(self):
        if not reapy.is_inside_reaper():
            dist_program.Program('HOLD').run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not reapy.is_inside_reaper():
            dist_program.Program('RELEASE').run()
        return False