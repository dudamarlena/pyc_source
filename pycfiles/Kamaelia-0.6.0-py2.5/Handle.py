# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/Handle.py
# Compiled at: 2008-10-19 12:19:52
import ThreadedComponent, time, Queue
print 'Polite Notice'
print '-------------'
print 'The code you are using includes using Axon.Handle. This code is'
print "currently experimental - we'd welcome any issues you may find/experience"
print 'with this code.'

class Handle(ThreadedComponent.threadedcomponent):
    Inboxes = {'_inbox': 'From the component to go to the outside world', 
       '_control': 'From the component to go to the outside world'}
    Outboxes = {'_outbox': 'From the outside world to go to the component', 
       '_signal': 'From the outside world to go to the component'}

    def __init__(self, someComponent):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Handle, self).__init__()
        self.comp = someComponent
        self.inboundData = Queue.Queue()
        self.outboundData = Queue.Queue()
        self.temp = {}

    def put(self, *args):
        self.inboundData.put(args)

    def _get(self):
        return self.outboundData.get_nowait()

    def get(self, boxname='outbox'):
        while 1:
            try:
                (data, outbox) = self._get()
                try:
                    self.temp[outbox].append(data)
                except KeyError:
                    self.temp[outbox] = [
                     data]

            except Queue.Empty:
                break

        try:
            X = self.temp[boxname][0]
            del self.temp[boxname][0]
        except KeyError:
            raise Queue.Empty
        except IndexError:
            raise Queue.Empty

        return X

    def main(self):
        """Main loop."""
        self.addChildren(self.comp)
        self.link((self, '_outbox'), (self.comp, 'inbox'))
        self.link((self, '_signal'), (self.comp, 'control'))
        self.link((self.comp, 'outbox'), (self, '_inbox'))
        self.link((self.comp, 'signal'), (self, '_control'))
        for child in self.children:
            child.activate()

        while not self.childrenDone():
            time.sleep(0.01)
            if not self.inboundData.empty():
                (data, box) = self.inboundData.get_nowait()
                if box == 'inbox':
                    self.send(data, '_outbox')
                if box == 'control':
                    self.send(data, '_signal')
            while self.dataReady('_inbox'):
                self.outboundData.put((self.recv('_inbox'), 'outbox'))

            while self.dataReady('_control'):
                self.outboundData.put((self.recv('_control'), 'signal'))

    def childrenDone(self):
        """Unplugs any children that have terminated, and returns true if there are no
          running child components left (ie. their microproceses have finished)
       """
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)

        return 0 == len(self.childComponents())


if __name__ == '__main__':
    print 'This is no longer like ThreadWrap - it is not supposed to be'
    print 'Usable in the usual manner for a component...'