# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/failed.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 756 bytes
import traceback
from ..util import log
from . import animation

class Failed(animation.Animation):
    __doc__ = "\n    An animation that's created when we fail to load or construct the\n    animation that was originally specified\n    "

    def __init__(self, layout, desc, exception):
        super().__init__(layout)
        self._set_runner({})
        log.error('Unable to create animation for %s', desc)
        debug = log.get_log_level() <= log.DEBUG
        if debug:
            try:
                msg = traceback.format_exc()
            except:
                msg = str(exception)

        else:
            msg = str(exception)
        log.error('\n%s', msg)
        self.desc = desc
        self.exception = exception
        self.empty = True