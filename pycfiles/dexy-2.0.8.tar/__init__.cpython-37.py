# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/__init__.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 141 bytes


def run(*args, **kwargs):
    from dexy.wrapper import Wrapper
    wrapper = Wrapper(*args, **kwargs)
    wrapper.run()
    wrapper.report()