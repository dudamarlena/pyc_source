# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/SampleTemplateComponent.py
# Compiled at: 2008-10-19 12:19:52
"""
Sample Template Component.
Use this as the basis for your components!

"""
from Axon.Component import component, scheduler

class CallbackStyleComponent(component):

    def __init__(self, label, looptimes, selfstart=0):
        super(CallbackStyleComponent, self).__init__()
        self.looptimes = looptimes
        self.label = label
        if selfstart:
            self.activate()

    def initialiseComponent(self):
        print 'DEBUG:', self.label, 'initialiseComponent'
        return 1

    def mainBody(self):
        print 'DEBUG: ', self.label, 'Now in the main loop'
        self.looptimes = self.looptimes - 1
        return self.looptimes

    def closeDownComponent(self):
        print 'DEBUG: ', self.label, 'closeDownComponent'


class StandardStyleComponent(component):

    def __init__(self, label, looptimes):
        super(CallbackStyleComponent, self).__init__()
        self.looptimes = looptimes
        self.label = label

    def main(self):
        print 'DEBUG:', self.label, 'initialiseComponent'
        yield 1
        while 1:
            print 'DEBUG: ', self.label, 'Now in the main loop'
            self.looptimes = self.looptimes - 1
            yield self.looptimes

        print 'DEBUG: ', self.label, 'closeDownComponent'


__kamaelia_components__ = (
 CallbackStyleComponent, StandardStyleComponent)
if __name__ == '__main__':
    myComponent('A', 3, 1)
    myComponent('B', 2).activate()
    scheduler.run.runThreads()