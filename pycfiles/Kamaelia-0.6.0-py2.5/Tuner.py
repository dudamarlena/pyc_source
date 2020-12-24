# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Device/DVB/Tuner.py
# Compiled at: 2008-10-19 12:19:52
"""====================================
DVB-T (Digital Terrestrial TV) Tuner
====================================

Tunes to the specified frequency, using the specified parameters, using a DVB
tuner device; then outputs packets from the received MPEG transport stream as
requested.

Example Usage
-------------

Record entire received MPEG transport stream, from a particular frequency and
set of tuning parameters to file::

    feparams = {
        "inversion" : dvb3.frontend.INVERSION_AUTO,
        "constellation" : dvb3.frontend.QAM_16,
        "code_rate_HP" : dvb3.frontend.FEC_3_4,
        "code_rate_LP" : dvb3.frontend.FEC_3_4,
    }
    
    Pipeline( OneShot( msg=["ADD", [0x2000] ] ),    # send the msg ["ADD", [0x2000]]
              Tuner(537.833330, feparams),
              SimpleFileWriter("dump.ts"),
            ).run()

Record just packets with packet ID (PID) 0 and 18::

    Pipeline( OneShot( msg=["ADD", [0, 18] ] ),
              Tuner(537833330.0, feparams),
              SimpleFileWriter("dump.ts"),
            ).run()

How does it work?
-----------------

Tuner tunes, using the specified tuning parameters to a DVB-T transmitted
multiplex. You can also specify which DVB tuner card (device) to use if there
is more than one in your system.

To start with it outputs nothing. To start or stop outputting packets, send
messages to the "inbox" inbox of the form::
    
    [ "ADD",    [pid, pid, ...] ]
    [ "REMOVE", [pid, pid, ...] ]
    
These instruct Tuner to output packets from the received multiplex with the
specified packet IDs (PIDs).

Most DVB tuner devices understand a special packet ID of 0x2000 to request the
entire transport stream of all packets with all IDs.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.

Tuning parameters
~~~~~~~~~~~~~~~~~

The tuning parameters come from the dvb3.frontend library. Specify them as a
dictionary::
    
    {
         "bandwidth"             : dvb3.frontend.BANDWIDTH_?_MHZ where ? is 6, 7 or 8
         "constellation"         : dvb3.frontend.QPSK, QAM_16 or QAM_64
         "hierarchy_information" : dvb3.frontend.HIERARCHY_? where ? is NONE, 1, 2 or 4
         "code_rate_HP"          : dvb3.frontend.FEC_X_Y where X/Y = 1/2, 2/3, 3/4, 5/6, 7/8
         "code_rate_LP"          : dvb3.frontend.FEC_X_Y where X/Y = 1/2, 2/3, 3/4, 5/6, 7/8
         "guard_interval"        : dvb3.frontend.GUARD_INTERVAL_1_? where ? is 32, 16, 8 or 4
         "transmission_mode"     : dvb3.frontend.TRANSMISSION_MODE_?K where ? is 2 or 8
         "inversion"             : dvb3.frontend.INVERSION_AUTO
    }
"""
import os, dvb3.frontend, dvb3.dmx, time, struct
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import shutdownMicroprocess, producerFinished
from Kamaelia.Chassis.Graphline import Graphline
DVB_PACKET_SIZE = 188
DVB_RESYNC = 'G'

class Tuner(threadedcomponent):
    """    Tuner(freq[,feparams][,card]) -> new Tuner component.
    
    Tunes the DVB-T card to the given frequency with the given parameters. Send
    (ADD, [PID list]) or (REMOVE, [PID list]) messages to its "inbox" inbox to
    cuase it to output MPEG transport stream packets (with the specified PIDs)
    from its "outbox" outbox.
    
    Keyword arguments:
        
    - freq      -- Frequency to tune to in MHz
    - feparams  -- Dictionary of parameters for the tuner front end (default={})
    - card      -- Which DVB device to use (default=0)
    """

    def __init__(self, freq, feparams={}, card=0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        self.freq = freq
        self.feparams = feparams
        self.card = card
        super(Tuner, self).__init__()

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        self.fe = dvb3.frontend.Frontend(self.card, blocking=0)
        self.tune_DVBT(self.freq, self.feparams)
        while self.notLocked():
            time.sleep(0.1)

        demuxers = {}
        fd = os.open('/dev/dvb/adapter' + str(self.card) + '/dvr0', os.O_RDONLY | os.O_NONBLOCK)
        while not self.shutdown():
            while self.dataReady('inbox'):
                cmd = self.recv('inbox')
                demuxers = self.handleCommand(cmd, demuxers)

            if demuxers:
                try:
                    data = os.read(fd, 2048)
                    self.send(data, 'outbox')
                except OSError:
                    self.sync()

            else:
                self.sync()

    def tune_DVBT(self, frequency, feparams={}):
        params = dvb3.frontend.OFDMParameters(frequency=(frequency * 1000 * 1000), **feparams)
        self.fe.set_frontend(params)

    def notLocked(self):
        """        Returns True if the frontend is not yet locked.
        Returns False if it is locked.
        """
        return self.fe.read_status() & dvb3.frontend.FE_HAS_LOCK == 0

    def addPID(self, pid):
        """        Adds the given PID to the transport stream that will be available
        in "/dev/dvb/adapter0/dvr0"
        """
        demuxer = dvb3.dmx.Demux(self.card, blocking=0)
        demuxer.set_pes_filter(pid, dvb3.dmx.DMX_IN_FRONTEND, dvb3.dmx.DMX_OUT_TS_TAP, dvb3.dmx.DMX_PES_OTHER, dvb3.dmx.DMX_IMMEDIATE_START)
        return demuxer

    def handleCommand(self, cmd, demuxers):
        if cmd[0] == 'ADD':
            pidlist = cmd[1]
            for pid in pidlist:
                if pid not in demuxers:
                    demuxers[pid] = self.addPID(pid)

            return demuxers
        elif cmd[0] == 'REMOVE':
            pidlist = cmd[1]
            for pid in pidlist:
                if pid in demuxers:
                    demuxers[pid].stop()
                    del demuxers[pid]

            return demuxers


__kamaelia_components__ = (
 Tuner,)