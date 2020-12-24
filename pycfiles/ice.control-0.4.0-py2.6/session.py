# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/repl/session.py
# Compiled at: 2010-08-27 06:32:04
import os
from zope.interface import implements
from zope.component import getUtilitiesFor
from interpreter import Interpreter
from interfaces import ISession

class Session:
    implements(ISession)
    input_buffer = ''
    history = []
    h_max = 10

    def __init__(self, context):
        self.interpreter = Interpreter({'__name__': '__console__', '__doc__': None, 
           'context': context})
        bootstrap = file(os.path.join(os.path.dirname(__file__), 'bootstrap.py'))
        for line in bootstrap.readlines():
            self.run(line)

        self.history = [
         '']
        return

    def update_history(self, source):
        try:
            self.history.remove(source)
        except ValueError:
            pass

        if source:
            self.history.insert(0, source)
        if len(self.history) > self.h_max:
            self.history = self.history[:self.h_max]

    def run(self, source):
        self.update_history(source)
        self.input_buffer += source
        result = self.interpreter.runsource(self.input_buffer)
        if result:
            self.input_buffer += '\n'
        else:
            self.input_buffer = ''
        return (
         result, self.interpreter.get_output())

    def get_history(self):
        return self.history