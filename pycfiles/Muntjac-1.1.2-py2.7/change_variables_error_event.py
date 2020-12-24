# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/gwt/server/change_variables_error_event.py
# Compiled at: 2013-04-04 15:36:36


class ChangeVariablesErrorEvent(object):

    def __init__(self, component, throwable, variableChanges):
        self._component = component
        self._throwable = throwable
        self._variableChanges = variableChanges

    def getThrowable(self):
        return self._throwable

    def getComponent(self):
        return self._component

    def getVariableChanges(self):
        return self._variableChanges