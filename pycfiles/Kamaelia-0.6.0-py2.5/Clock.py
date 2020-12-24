# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Clock.py
# Compiled at: 2008-10-19 12:19:52
"""========================
Cheap And Cheerful Clock
========================

Outputs the message True repeatedly. The interval between messages is the
parameter "interval" specified at the creation of the component.

This component is useful because it allows another component to sleep,
not using any CPU time, but waking periodically (components are unpaused
when they are sent a message).

Why is it "cheap and cheerful"?

...Because it uses a thread just for itself. All clocks could share a
single thread if some services kung-fu was pulled.
Opening lots of threads is a bad thing - they have much greater
overhead than normal generator-based components. However, the 
one-thread-per-clock approach used here is many times shorter
and simpler than one using services.
"""
import time
from Axon.ThreadedComponent import threadedcomponent

class CheapAndCheerfulClock(threadedcomponent):
    """Outputs the message True every interval seconds"""

    def __init__(self, interval):
        super(CheapAndCheerfulClock, self).__init__()
        self.interval = interval

    def main(self):
        while 1:
            self.send(True, 'outbox')
            time.sleep(self.interval)


__kamaelia_components__ = (CheapAndCheerfulClock,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.DataSource import TriggeredSource
    from Kamaelia.Util.Console import ConsoleEchoer
    pipeline(CheapAndCheerfulClock(3.0), TriggeredSource('Fish\n'), ConsoleEchoer()).run()