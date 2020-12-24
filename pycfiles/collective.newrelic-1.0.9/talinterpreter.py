# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/talinterpreter.py
# Compiled at: 2013-12-24 05:41:42
from zope.tal.talinterpreter import TALInterpreter
import newrelic.agent
from collective.newrelic.utils import logger
original_function = TALInterpreter.__call__

def monkeypatch(self):
    probable_name = self.program[2][1]
    name = 'Value (non-file)'
    if type(probable_name) in [str, unicode]:
        name = probable_name.split('/')
        name = name[(-1)]
    newrelic_monkeypatch = newrelic.agent.FunctionTraceWrapper(original_function, name, 'Zope/TAL')
    newrelic_monkeypatch(self)


TALInterpreter.__call__ = monkeypatch
logger.info('Patched zope.tal.talinterpreter:TALInterpreter.__call__ with instrumentation')