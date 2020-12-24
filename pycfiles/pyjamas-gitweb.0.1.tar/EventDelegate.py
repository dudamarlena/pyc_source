# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/EventDelegate.py
# Compiled at: 2008-09-03 09:02:13
from pyjamas.__pyjamas__ import JS

class EventDelegate:
    """
      Create the equivalent of a bound method.  This also prepends extra 
      args, if any, to the called method's argument list when it calls it.
      
      Pass the method name you want to implement (javascript doesn't
      support callables).
      
      @type args: list
      @param args: If given, the arguments will be prepended to the 
                   arguments passed to the event callback
   """

    def __init__(self, eventMethodName, obj, method, *args):
        self.obj = obj
        self.method = method
        self.args = args
        JS('this[eventMethodName] = this.onEvent;')

    def onEvent(self, *args):
        self.method.apply(self.obj, self.args.l.concat(args.l))