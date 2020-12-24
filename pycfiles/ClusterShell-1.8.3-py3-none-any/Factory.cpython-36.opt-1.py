# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Engine/Factory.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 2594 bytes
"""
Engine Factory to select the best working event engine for the current
version of Python and Operating System.
"""
import logging
from ClusterShell.Engine.Engine import EngineNotSupportedError
from ClusterShell.Engine.EPoll import EngineEPoll
from ClusterShell.Engine.Poll import EnginePoll
from ClusterShell.Engine.Select import EngineSelect

class PreferredEngine(object):
    __doc__ = '\n    Preferred Engine selection metaclass (DP Abstract Factory).\n    '
    engines = {EngineEPoll.identifier: EngineEPoll, 
     EnginePoll.identifier: EnginePoll, 
     EngineSelect.identifier: EngineSelect}

    def __new__(cls, hint, info):
        """
        Create a new preferred Engine.
        """
        if not hint or hint == 'auto':
            for engine_class in [EngineEPoll, EnginePoll, EngineSelect]:
                try:
                    return engine_class(info)
                except EngineNotSupportedError:
                    pass

            raise RuntimeError('FATAL: No supported ClusterShell.Engine found')
        else:
            engines = cls.engines.copy()
        try:
            tryengine = engines.pop(hint)
            while True:
                try:
                    return tryengine(info)
                except EngineNotSupportedError:
                    if len(engines) == 0:
                        raise

                tryengine = engines.popitem()[1]

        except KeyError:
            msg = 'Invalid engine identifier: %s' % hint
            logging.getLogger(__name__).error(msg)
            raise