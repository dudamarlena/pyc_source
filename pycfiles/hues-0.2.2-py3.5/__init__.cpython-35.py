# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hues/__init__.py
# Compiled at: 2016-10-02 13:05:03
# Size of source mod 2**32: 494 bytes
from .huestr import HueString as huestr
from .console import Config, SimpleConsole, PowerlineConsole
__version__ = (0, 2, 2)
conf = Config()
if conf.opts.theme == 'simple':
    console = SimpleConsole(conf=conf)
elif conf.opts.theme == 'powerline':
    console = PowerlineConsole(conf=conf)
log = console.log
info = console.info
warn = console.warn
error = console.error
success = console.success
del conf
__all__ = ('huestr', 'console', 'log', 'info', 'warn', 'error', 'success')