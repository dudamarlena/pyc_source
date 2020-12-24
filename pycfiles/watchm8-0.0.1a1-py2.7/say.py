# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/actions/say.py
# Compiled at: 2017-09-11 08:39:54
from ._base import BaseAction

class Event(BaseAction):
    """Log event to info level

    Example:
        .. code-block:: yaml

            do:
                kind: .say.Event
    """

    def __call__(self, event, emitter):
        self._log.info(str(event))