# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/breezekay/Dropbox/Codes/ez/py.ez.co/comb.ez.co/comb/demo/list.py
# Compiled at: 2014-10-20 03:45:00
import comb.slot, sys
from time import sleep
import threading

class Slot(comb.slot.Slot):

    def initialize(self):
        """Hook for initialization.

        This block is execute before thread initial

       Example::

           class UserSlot(Slot):
               def initialize(self):
                   ...

               def slot(self, result):
                   ...

       """
        if self.combd.extra_loader.actions.get('act1'):
            print 'Catch act1 action, program will exit.'
            sys.exit(0)
        if self.combd.extra_loader.options.get('opt1'):
            print 'Catch opt1 option, program will exit.'
            sys.exit(0)
        if self.debug:
            if sys.version_info[0] == 2:
                self.todo_list = range(1000, 2000)
            else:
                self.todo_list = list(range(1000, 2000))
            print 'You set debug flag,prepare todo_list, from 1000,2000'
        else:
            if sys.version_info[0] == 2:
                self.todo_list = range(1, 1000)
            else:
                self.todo_list = list(range(1, 1000))
            print 'prepare todo_list, from 1,1000'
        print 'current threads set:%d,cycle is %d,cycle_max is %d' % (self.threads_num, self.sleep, self.sleep_max)
        print 'slot start now,will sleep 2 second.'
        sleep(2)
        print 'slot will pop up todo list.sleep 2 second.'
        sleep(2)
        print self.todo_list

    def __enter__(self):
        if not self.todo_list:
            print 'Finish,this must be return *False* when no data found.'
            return False
        else:
            next = self.todo_list.pop()
            return next

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'call __exit__'

    def slot(self, result):
        print (
         'call slot,found number is:', result)
        if self.combd.extra_loader.options.get('opt1'):
            pass

    @staticmethod
    def options():
        return (
         'Useage  comb.slot [actions] [options]',
         '',
         'Actions',
         ('@act1', 'act1 flag,try set it.'),
         'Options:',
         ('--opt1', 'set opt1 flag'),
         '',
         ('--help', 'print help document', '-h'),
         'More:',
         'Hi,This is a demo.Useage synax please refer Cliez package.')