# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/knxsonos/knx.py
# Compiled at: 2016-04-09 16:43:06
from EIBConnection import EIBConnection, EIBBuffer, EIBAddr
from EIBConnection import individual2string, readgaddr
from sys import argv, exit
from threading import Thread
import logging

class KnxListenGrpAddr(Thread):

    def __init__(self, url, zone_name, gaddr, action):
        Thread.__init__(self)
        self.logger = logging.getLogger('knxsonos')
        self.name = '%s_%s' % (zone_name.encode('utf-8'), gaddr)
        self.zone_name = zone_name
        self.gaddr = gaddr
        self.stopping = False
        self.daemon = True
        if type(action) == type([]):
            self.action = action
        else:
            self.action = [
             action]
        try:
            self.con = EIBConnection()
        except:
            self.logger.error('Could not instanciate EIBConnection')
            exit(1)

        if self.con.EIBSocketURL(url) != 0:
            self.logger.error('Could not connect to: %s' % url)
            exit(1)
        dest = readgaddr(self.gaddr)
        if self.con.EIBOpenT_Group(dest, 0) == -1:
            self.logger.error('Connect failed')
            exit(1)

    def stop(self):
        self.stopping = True
        self.join(0.1)
        if self.isAlive():
            self.logger.warning('Thread %s did not stop!' % self.name)

    def run(self):
        self.logger.debug('KNX: Entering read loop...')
        while not self.stopping:
            try:
                src = EIBAddr()
                buf = EIBBuffer()
                length = self.con.EIBGetAPDU_Src(buf, src)
                if length < 2:
                    self.logger.error('Read failed')
                    exit(1)
                if buf.buffer[0] & 3 or buf.buffer[1] & 192 == 192:
                    self.logger.warning('Unknown APDU from %s' % individual2string(src.data))
                self.logger.info('KNX:  Group address %s received from %s' % (
                 self.gaddr,
                 individual2string(src.data)))
                for a, p in self.action:
                    if callable(a):
                        if p == None:
                            a(self.zone_name)
                        else:
                            a(self.zone_name, p)
                    else:
                        self.logger.error('KNX:  Can not call action: %s' % str(a))

            except Exception as e:
                self.logger.error(e)

        self.logger.info('KNX:  Ending thread...')
        self.logger.info('KNX:  Closing...')
        self.con.EIBClose()
        return


class KnxInterface:

    def __init__(self, url, action_table):
        self.gaddrs = [ KnxListenGrpAddr(url, zn, g, a) for zn, g, a in action_table
                      ]

    def start(self):
        for g in self.gaddrs:
            g.start()

    def stop(self):
        for g in self.gaddrs:
            g.stop()