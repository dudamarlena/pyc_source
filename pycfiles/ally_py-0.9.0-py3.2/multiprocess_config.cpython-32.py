# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sql_alchemy/multiprocess_config.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Oct 24, 2012

@package: support sqlalchemy
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configuration used for wraping the connection pool to properly support multiple processes.
"""
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