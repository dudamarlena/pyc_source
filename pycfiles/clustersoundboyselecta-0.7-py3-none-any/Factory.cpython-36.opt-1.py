# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Engine/Factory.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 2594 bytes
__doc__ = '\nEngine Factory to select the best working event engine for the current\nversion of Python and Operating System.\n'
import logging
from ClusterShell.Engine.Engine import EngineNotSupportedError
from ClusterShell.Engine.EPoll import EngineEPoll
from ClusterShell.Engine.Poll import EnginePoll
from ClusterShell.Engine.Select import EngineSelect

class PreferredEngine(object):
    """PreferredEngine"""
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