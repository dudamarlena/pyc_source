# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/synth/midi/MidiEvent.py
# Compiled at: 2015-04-18 11:05:46
import utils, sys

class MidiEvent(object):

    def __init__(self):
        self.event_types = {8: 'Note off', 
           9: 'Note on', 
           10: 'Polyphonic key pressure (aftertouch)', 
           11: 'Control change', 
           12: 'Program change', 
           13: 'Channel pressure (aftertouch)', 
           14: 'Pitch bend change'}

    def reset(self):
        self.channel = None
        self.meta_event = None
        self.event_type = None
        self.param1 = None
        self.param2 = None
        self.data = None
        self.delta_time = None
        self.start_time = None
        self.stop_time = None
        self.last_event_of_track = False
        self.system_common_message = None
        return

    def parse_midi_event(self, fp):
        """Parse a MIDI event.

        Return a dictionary and the number of bytes read.
        """
        self.reset()
        chunk_size = 0
        try:
            ec = utils.bytes_to_int(fp.read(1))
            chunk_size += 1
        except:
            raise IOError("Couldn't read event type and channel data from file.")

        event_type = (ec & 240) >> 4
        channel = ec & 15
        if event_type < 8:
            return chunk_size
        self.event_type = event_type
        self.channel = channel
        if event_type == 15:
            chunk_size += self.parse_meta_event(fp)
        elif event_type in (12, 13):
            chunk_size += self.parse_program_change_and_channel_aftertouch_events(fp)
        else:
            chunk_size += self.parse_misc_events(fp)
        return chunk_size

    def parse_meta_event(self, fp):
        meta_event = utils.bytes_to_int(fp.read(1))
        length, chunk_delta = utils.parse_varbyte_as_int(fp)
        if meta_event == 47:
            self.last_event_of_track = True
        data = fp.read(length)
        chunk_size = 1 + chunk_delta + length
        self.meta_event = meta_event
        self.data = data
        return chunk_size

    def parse_program_change_and_channel_aftertouch_events(self, fp):
        try:
            param1 = fp.read(1)
        except:
            raise IOError("Couldn't read MIDI event parameters from file.")

        self.param1 = utils.bytes_to_int(param1)
        return 1

    def parse_misc_events(self, fp):
        try:
            param1 = fp.read(1)
            param2 = fp.read(1)
        except:
            raise IOError("Couldn't read MIDI event parameters from file.")

        self.param1 = utils.bytes_to_int(param1)
        self.param2 = utils.bytes_to_int(param2)
        return 2

    def parse_system_common_message(self, event_type):
        self.system_common_message = event_type

    def __repr__(self):
        time = '%d' % self.start_time
        if self.stop_time is not None:
            time += '-%d' % self.stop_time
        et = 'Event %s' % self.event_type
        if self.event_type in self.event_types:
            et = self.event_types[self.event_type]
        if self.meta_event is not None:
            et = 'Meta event %d' % self.meta_event
        channel = self.channel
        if self.meta_event is not None:
            channel = ''
        params = 'param1: %s' % self.param1
        if self.param2 is not None:
            params += ', param2: %s' % self.param2
        if self.meta_event is not None:
            params = 'data: %s' % self.data
        return '%s: %s %s %s' % (time, et, channel, params)