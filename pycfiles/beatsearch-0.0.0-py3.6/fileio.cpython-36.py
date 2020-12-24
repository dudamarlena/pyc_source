# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\midi\fileio.py
# Compiled at: 2018-03-19 10:03:58
# Size of source mod 2**32: 6544 bytes
from warnings import *
from .containers import *
from .events import *
from struct import unpack, pack
from .constants import *
from .util import *

class FileReader(object):

    def read(self, midifile):
        pattern = self.parse_file_header(midifile)
        for track in pattern:
            self.parse_track(midifile, track)

        return pattern

    def parse_file_header(self, midifile):
        magic = midifile.read(4)
        if magic != b'MThd':
            raise TypeError('Bad header in MIDI file.')
        data = unpack('>LHHH', midifile.read(10))
        hdrsz = data[0]
        format = data[1]
        tracks = [Track() for x in range(data[2])]
        resolution = data[3]
        if hdrsz > DEFAULT_MIDI_HEADER_SIZE:
            midifile.read(hdrsz - DEFAULT_MIDI_HEADER_SIZE)
        return Pattern(tracks=tracks, resolution=resolution, format=format)

    def parse_track_header(self, midifile):
        magic = midifile.read(4)
        if magic != b'MTrk':
            raise TypeError('Bad track header in MIDI file: ' + magic)
        trksz = unpack('>L', midifile.read(4))[0]
        return trksz

    def parse_track(self, midifile, track):
        self.RunningStatus = None
        trksz = self.parse_track_header(midifile)
        trackdata = iter(midifile.read(trksz))
        while True:
            try:
                event = self.parse_midi_event(trackdata)
                track.append(event)
            except StopIteration:
                break

    def parse_midi_event(self, trackdata):
        tick = read_varlen(trackdata)
        stsmsg = ord(bytearray([next(trackdata)]))
        if MetaEvent.is_event(stsmsg):
            cmd = ord(bytearray([next(trackdata)]))
            if cmd not in EventRegistry.MetaEvents:
                warn('Unknown Meta MIDI Event: ' + repr(cmd), Warning)
                cls = UnknownMetaEvent
            else:
                cls = EventRegistry.MetaEvents[cmd]
            datalen = read_varlen(trackdata)
            data = [ord(bytearray([next(trackdata)])) for x in range(datalen)]
            return cls(tick=tick, data=data, metacommand=cmd)
        if SysexEvent.is_event(stsmsg):
            data = []
            while True:
                datum = ord(bytearray([next(trackdata)]))
                if datum == 247:
                    break
                data.append(datum)

            return SysexEvent(tick=tick, data=data)
        else:
            key = stsmsg & 240
            if key not in EventRegistry.Events:
                assert self.RunningStatus, 'Bad byte value'
                data = []
                key = self.RunningStatus & 240
                cls = EventRegistry.Events[key]
                channel = self.RunningStatus & 15
                data.append(stsmsg)
                data += [ord(bytearray([next(trackdata)])) for x in range(cls.length - 1)]
                return cls(tick=tick, channel=channel, data=data)
            self.RunningStatus = stsmsg
            cls = EventRegistry.Events[key]
            channel = self.RunningStatus & 15
            data = [ord(bytearray([next(trackdata)])) for x in range(cls.length)]
            return cls(tick=tick, channel=channel, data=data)
        raise Warning('Unknown MIDI Event: ' + repr(stsmsg))


class FileWriter(object):

    def write(self, midifile, pattern):
        self.write_file_header(midifile, pattern)
        for track in pattern:
            self.write_track(midifile, track)

    def write_file_header(self, midifile, pattern):
        packdata = pack('>LHHH', 6, pattern.format, len(pattern), pattern.resolution)
        midifile.write(b'MThd' + packdata)

    def write_track(self, midifile, track):
        buf = b''
        self.RunningStatus = None
        for event in track:
            buf += self.encode_midi_event(event)

        buf = self.encode_track_header(len(buf)) + buf
        midifile.write(buf)

    def encode_track_header(self, trklen):
        return b'MTrk' + pack('>L', trklen)

    def encode_midi_event(self, event):
        ret = bytearray()
        ret += write_varlen(event.tick)
        if isinstance(event, MetaEvent):
            ret += bytearray([event.statusmsg]) + bytearray([event.metacommand])
            ret += write_varlen(len(event.data))
            ret += bytearray(event.data)
        else:
            if isinstance(event, SysexEvent):
                ret += bytearray([240])
                ret += bytearray(event.data)
                ret += bytearray([247])
            else:
                if isinstance(event, Event):
                    if not self.RunningStatus or self.RunningStatus.statusmsg != event.statusmsg or self.RunningStatus.channel != event.channel:
                        self.RunningStatus = event
                        ret += bytearray([event.statusmsg | event.channel])
                    ret += bytearray(event.data)
                else:
                    raise ValueError('Unknown MIDI Event: ' + str(event))
        return ret


def write_midifile(midifile, pattern):
    if type(midifile) in (str, str):
        midifile = open(midifile, 'wb')
    writer = FileWriter()
    return writer.write(midifile, pattern)


def read_midifile(midifile):
    if type(midifile) in (str, str):
        midifile = open(midifile, 'rb')
    reader = FileReader()
    return reader.read(midifile)