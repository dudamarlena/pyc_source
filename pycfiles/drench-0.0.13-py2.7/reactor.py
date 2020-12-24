# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/drench/reactor.py
# Compiled at: 2013-12-10 14:37:29
from collections import defaultdict
import select
from collections import namedtuple
select_response = namedtuple('select_response', 'readable writable exceptional')

class Reactor(object):

    def __init__(self):
        self.is_running = True
        self.subscribed = defaultdict(list)
        self.select_list = []
        self.out_sock = None
        return

    def subscribe(self, callback, event):
        self.subscribed[event].append(callback)

    def trigger(self, event):
        for callback in self.subscribed[event]:
            callback()

        self.subscribed[event] = []

    def add_listeners(self, listeners):
        for listener in listeners:
            self.select_list.append(listener)

    def event_loop(self):
        while self.is_running:
            doable_lists = select_response(*select.select(self.select_list, [], [], 1))
            if not doable_lists.readable:
                for i in self.select_list:
                    if 'read_timeout' in dir(i):
                        i.read_timeout()

            for i in doable_lists.readable:
                i.read()
                wclos = i.write
                self.subscribed['write'].append(wclos)

            self.trigger('logic')
            self.trigger('write')


def main():
    reactor = Reactor()
    reactor.event_loop()


if __name__ == '__main__':
    main()