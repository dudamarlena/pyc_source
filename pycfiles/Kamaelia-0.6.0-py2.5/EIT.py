# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Device/DVB/EIT.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.Device.DVB.Core import DVB_Multiplex, DVB_Demuxer
from Axon.Component import component
import struct
from Axon.Ipc import shutdownMicroprocess, producerFinished

class PSIPacketReconstructor(component):
    """    Takes DVB Transport stream packets for a given PID and reconstructs the
    PSI packets from within the stream.
    
    Will only handle stream from a single PID.
    """

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        buffer = ''
        nextCont = None
        while not self.shutdown():
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                byte = ord(data[1])
                start_indicator = byte & 64 != 0
                byte = ord(data[3])
                adaption = (byte & 48) >> 4
                contcount = byte & 15
                if nextCont == None and start_indicator or nextCont == contcount:
                    if adaption == 1:
                        payload_start = 4
                    elif adaption == 3:
                        payload_start = 5 + ord(data[4])
                    else:
                        continue
                    if start_indicator:
                        prevstart = payload_start
                        payload_start = prevstart + ord(data[prevstart]) + 1
                        buffer = buffer + data[prevstart + 1:payload_start]
                        if len(buffer) and nextCont != None:
                            self.send(buffer, 'outbox')
                        buffer = ''
                    buffer = buffer + data[payload_start:]
                    nextCont = contcount + 1 & 15
                else:
                    nextCont = None
                    buffer = ''

            self.pause()
            yield 1

        return


class EITPacketParser(component):
    """    Parses EIT packets and extracts NOW & NEXT short event descriptions for
    channels within this transport stream.
    
    (Ignores events belonging to other multiplexes)
    """
    Inboxes = {'inbox': 'PES packets', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'Parsed NOW and NEXT EIT events', 'signal': 'NOT USED'}

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        while not self.shutdown():
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                msg = {}
                s = struct.unpack('>BHHBBBHHBB', data[:14])
                table_id = s[0]
                syntax = s[1] & 32768
                section_length = s[1] & 4095
                service_id = s[2]
                version = s[3] >> 1 & 31
                current_next = s[3] & 1
                section_num = s[4]
                last_section = s[5]
                ts_id = s[6]
                net_id = s[7]
                seg_last_sect = s[8]
                last_table_id = s[9]
                data = data[:3 + section_length]
                if table_id != 78:
                    continue
                if not syntax:
                    print 'wrong syntax'
                    continue
                if not current_next:
                    continue
                subtable_id = (table_id, service_id, ts_id, net_id)
                if crc32(data):
                    print 'EIT packet CRC error'
                    continue
                msg['service'] = service_id
                msg['transportstream'] = ts_id
                pos = 14
                while pos < len(data) - 4:
                    e = struct.unpack('>HHBBBBBBH', data[pos:pos + 12])
                    event_id = e[0]
                    date = parseMJD(e[1])
                    time = (unBCD(e[2]), unBCD(e[3]), unBCD(e[4]))
                    duration = (unBCD(e[5]), unBCD(e[6]), unBCD(e[7]))
                    running_status = (e[8] & 57344) >> 13
                    free_CA_mode = e[8] & 4096
                    descriptors_len = e[8] & 4095
                    if running_status in (1, 2):
                        msg['when'] = 'NEXT'
                    elif running_status in (3, 4):
                        msg['when'] = 'NOW'
                    msg['startdate'] = date
                    msg['starttime'] = time
                    msg['duration'] = duration
                    pos = pos + 12
                    descriptors_end = pos + descriptors_len
                    while pos < descriptors_end:
                        desc_tag = ord(data[pos])
                        desc_len = ord(data[(pos + 1)])
                        if desc_tag == 77:
                            lang = data[pos + 2:pos + 5]
                            namelen = ord(data[(pos + 5)])
                            name = data[pos + 6:pos + 6 + namelen]
                            textlen = ord(data[(pos + 6 + namelen)])
                            text = data[pos + 7 + namelen:pos + 7 + namelen + textlen]
                            msg['name'] = name
                            msg['description'] = text
                        pos = pos + 2 + desc_len

                    self.send(msg, 'outbox')

            self.pause()
            yield 1


def crc32(data):
    poly = 79764919
    crc = 4294967295
    for byte in data:
        byte = ord(byte)
        for bit in range(7, -1, -1):
            z32 = crc >> 31
            crc = crc << 1
            if byte >> bit & 1 ^ z32:
                crc = crc ^ poly
            crc = crc & 4294967295

    return crc


def parseMJD(MJD):
    """Parse 16 bit unsigned int containing Modified Julian Date, as per DVB-SI spec
    returning year,month,day"""
    YY = int((MJD - 15078.2) / 365.25)
    MM = int((MJD - 14956.1 - int(YY * 365.25)) / 30.6001)
    D = MJD - 14956 - int(YY * 365.25) - int(MM * 30.6001)
    K = 0
    if MM == 14 or MM == 15:
        K = 1
    return (1900 + YY + K, MM - 1 - K * 12, D)


def unBCD(byte):
    return (byte >> 4) * 10 + (byte & 15)


class NowNextChanges(component):
    """    Simple attempt to filter DVB now and next info for multiple services,
    such that we only send output when the data changes.
    """

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        current = {}
        while not self.shutdown():
            while self.dataReady('inbox'):
                event = self.recv('inbox')
                if event['when'] != 'NOW':
                    continue
                uid = (
                 event['service'], event['transportstream'])
                if current.get(uid, None) != event:
                    current[uid] = event
                    self.send(current[uid], 'outbox')

            self.pause()
            yield 1

        return


class NowNextServiceFilter(component):
    """    Filters now/next event data for only specified services.
    """

    def __init__(self, *services):
        super(NowNextServiceFilter, self).__init__()
        self.services = services

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        while not self.shutdown():
            while self.dataReady('inbox'):
                event = self.recv('inbox')
                if event['service'] in self.services:
                    self.send(event, 'outbox')

            self.pause()
            yield 1


class TimeAndDatePacketParser(component):
    """    Parses "Time and Date" packets.
    """
    Inboxes = {'inbox': 'PES packets', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'Parsed date and time', 'signal': 'NOT USED'}

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def main(self):
        while not self.shutdown():
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                msg = {}
                s = struct.unpack('>BHHBBB', data[:8])
                table_id = s[0]
                syntax = s[1] & 32768
                section_length = s[1] & 4095
                data = data[:3 + section_length]
                if table_id != 112:
                    continue
                if syntax:
                    print 'wrong syntax'
                    continue
                date = parseMJD(s[2])
                time = (unBCD(s[3]), unBCD(s[4]), unBCD(s[5]))
                msg['date'] = date
                msg['time'] = time
                self.send(msg, 'outbox')

            self.pause()
            yield 1


__kamaelia_components__ = (
 PSIPacketReconstructor, EITPacketParser, NowNextChanges, NowNextServiceFilter, TimeAndDatePacketParser)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.Writing import SimpleFileWriter
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Chassis.Graphline import Graphline
    from Kamaelia.Util.Console import ConsoleEchoer
    import dvb3.frontend
    feparams = {'inversion': dvb3.frontend.INVERSION_AUTO, 
       'constellation': dvb3.frontend.QAM_16, 
       'code_rate_HP': dvb3.frontend.FEC_3_4, 
       'code_rate_LP': dvb3.frontend.FEC_3_4}
    Graphline(SOURCE=DVB_Multiplex(505833330.0 / 1000000.0, [18, 20, 600, 601], feparams), DEMUX=DVB_Demuxer({18: ['_EIT_'], 20: ['_DATETIME_']}), EIT=Pipeline(PSIPacketReconstructor(), EITPacketParser(), NowNextServiceFilter(4164, 4228), NowNextChanges(), ConsoleEchoer()), DATETIME=Pipeline(PSIPacketReconstructor(), TimeAndDatePacketParser(), ConsoleEchoer()), linkages={('SOURCE', 'outbox'): ('DEMUX', 'inbox'), ('DEMUX', '_EIT_'): ('EIT', 'inbox'), 
       ('DEMUX', '_DATETIME_'): ('DATETIME', 'inbox')}).run()