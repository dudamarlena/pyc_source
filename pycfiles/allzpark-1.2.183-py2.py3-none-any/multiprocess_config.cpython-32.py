# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/sql_alchemy/multiprocess_config.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Oct 24, 2012\n\n@package: support sqlalchemy\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the configuration used for wraping the connection pool to properly support multiple processes.\n'
from ally.container import support
from ally.support.sqlalchemy.pool import SingletonProcessWrapper
from sqlalchemy.engine.base import Engine
from ally.support.util_sys import callerLocals

def enableMultiProcessPool():
    """
    Wraps all the engines in the current assembly with a pool that allows for working on multiple processes.
    """

    def present(engine):
        """
        Used for listening to all sql alchemy engines that are created in order to wrap the engine pool with a pool that can
        handle multiple processors.
        """
        if not isinstance(engine.pool, SingletonProcessWrapper):
            engine.pool = SingletonProcessWrapper(engine.pool)

    support.listenToEntities(Engine, listeners=present, module=callerLocals(), all=True)