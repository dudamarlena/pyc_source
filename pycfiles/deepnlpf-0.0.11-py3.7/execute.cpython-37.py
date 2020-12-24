# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/core/execute.py
# Compiled at: 2020-04-15 17:57:18
# Size of source mod 2**32: 591 bytes
"""
    Date 16/08/2019
"""

class Execute(object):
    __doc__ = ' Execute Scripts External in Outher Language Programation. '

    def __init__(self):
        pass

    def run_r(self, script, *args):
        import rpy2.robjects as ro
        r = ro.r
        r.source(script)
        return (r.main)(*args)

    def run_java(self, jar_file, *args):
        try:
            import subprocess
            return subprocess.check_output(['java', '-jar', jar_file, *args], shell=False)
        except Exception as err:
            try:
                print(err)
            finally:
                err = None
                del err