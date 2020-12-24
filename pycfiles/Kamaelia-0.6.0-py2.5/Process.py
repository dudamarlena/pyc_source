# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/experimental/Process.py
# Compiled at: 2008-10-19 12:19:52
import Axon
from Axon.Scheduler import scheduler
import Axon.experimental._pprocess_support, pprocess, time, pprint

class ProcessWrapComponent(object):

    def __init__(self, somecomponent):
        self.exchange = pprocess.Exchange()
        self.channel = None
        self.inbound = []
        self.thecomponent = somecomponent
        self.ce = None
        self.tick = time.time()
        return

    def ticking(self):
        if time.time() - self.tick > 1:
            self.tick = time.time()

    def run(self, channel):
        self.exchange.add(channel)
        self.channel = channel
        from Axon.experimental._pprocess_support import likefile, background
        background(zap=True).start()
        time.sleep(0.1)
        self.ce = likefile(self.thecomponent)
        for i in self.main():
            pass

    def activate(self):
        channel = pprocess.start(self.run)
        return channel

    def main(self):
        t = 0
        while 1:
            if time.time() - t > 0.2:
                t = time.time()
            if self.exchange.ready(0):
                chan = self.exchange.ready(0)[0]
                D = chan._receive()
                self.ce.put(*D)
            D = self.ce.anyReady()
            if D:
                for boxname in D:
                    D = self.ce.get(boxname)
                    self.channel._send((D, boxname))

            yield 1


def ProcessPipeline(*components):
    exchange = pprocess.Exchange()
    debug = False
    chans = []
    for comp in components:
        A = ProcessWrapComponent(comp)
        chan = A.activate()
        chans.append(chan)
        exchange.add(chan)

    mappings = {}
    for i in xrange(len(components) - 1):
        mappings[(chans[i], 'outbox')] = (
         chans[(i + 1)], 'inbox')
        mappings[(chans[i], 'signal')] = (chans[(i + 1)], 'control')

    while 1:
        for chan in exchange.ready(0):
            D = chan._receive()
            try:
                dest = mappings[(chan, D[1])]
                dest[0]._send((D[0], dest[1]))
            except KeyError:
                if debug:
                    print 'WARNING: Data sent to outbox not linked to anywhere. Error?'
                    print 'chan, D[1] D[0]', chan, D[1], repr(D[0])
                    pprint.pprint(mappings)

        time.sleep(0.1)


def ProcessGraphline(**graphline_spec):
    chans = []
    count = 0
    component_to_chan = {}
    mappings = {}
    debug = graphline_spec.get('__debug', False)
    chan_to_compname = {}
    exchange = pprocess.Exchange()
    for comp in graphline_spec:
        if comp != 'linkages' and comp[:2] != '__':
            A = ProcessWrapComponent(graphline_spec[comp])
            chan = A.activate()
            chans.append(chan)
            chan_to_compname[chan] = comp
            exchange.add(chan)
            component_to_chan[comp] = chan
            count += 1

    linkages = graphline_spec.get('linkages', {})
    for source in linkages:
        sink = linkages[source]
        mappings[(component_to_chan[source[0]], source[1])] = (component_to_chan[sink[0]], sink[1])

    while 1:
        for chan in exchange.ready(0):
            D = chan._receive()
            try:
                dest = mappings[(chan, D[1])]
                dest[0]._send((D[0], dest[1]))
            except KeyError:
                if debug:
                    print 'WARNING: Data sent to outbox not linked to anywhere. Error?'
                    print 'chan, D[1] D[0]', chan, D[1], repr(D[0])
                    pprint.pprint(mappings)

        time.sleep(0.001)


class ProcessPipelineComponent(Axon.Component.component):

    def __init__(self, *components, **argd):
        super(ProcessPipelineComponent, self).__init__(**argd)
        self.components = components

    def main(self):
        exchange = pprocess.Exchange()
        chans = []
        for comp in self.components:
            A = ProcessWrapComponent(comp)
            chan = A.activate()
            chans.append(chan)
            exchange.add(chan)

        mappings = {}
        for i in xrange(len(self.components) - 1):
            mappings[(chans[i], 'outbox')] = (
             chans[(i + 1)], 'inbox')
            mappings[(chans[i], 'signal')] = (chans[(i + 1)], 'control')

        while 1:
            for chan in exchange.ready(0):
                D = chan._receive()
                dest = mappings[(chan, D[1])]
                if chan != chans[(-1)]:
                    dest[0]._send((D[0], dest[1]))
                else:
                    self.send(D[0], D[1])

            while self.dataReady('inbox'):
                D = self.recv('inbox')
                chans[0]._send((D, 'inbox'))

            while self.dataReady('control'):
                D = self.recv('inbox')
                chans[0]._send((D, 'control'))

            yield 1


if __name__ == '__main__':
    from Kamaelia.UI.Pygame.Text import TextDisplayer, Textbox
    ProcessPipeline(Textbox(position=(20, 340), text_height=36, screen_width=900, screen_height=200, background_color=(130,
                                                                                                                       0,
                                                                                                                       70), text_color=(255,
                                                                                                                                        255,
                                                                                                                                        255)), TextDisplayer(position=(20,
                                                                                                                                                                       90), text_height=36, screen_width=900, screen_height=200, background_color=(130,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   70), text_color=(255,
                                                                                                                                                                                                                                                                    255,
                                                                                                                                                                                                                                                                    255)))