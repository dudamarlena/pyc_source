# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/synth/instruments/SynthInstrument.py
# Compiled at: 2015-04-18 11:05:46
from synth.envelopes import SegmentAmplitudeEnvelope
from synth.oscillator import OscillatorWithAmplitudeEnvelope
from synth.instruments.BaseInstrument import BaseInstrument

class SynthInstrument(BaseInstrument):

    def __init__(self, options, note_envelope):
        super(SynthInstrument, self).__init__(options, note_envelope)

    def init_note(self, options, note, freq):
        amp_env = SegmentAmplitudeEnvelope()
        amp_env.add_segment(1.0, 1000)
        amp_env.add_segment(0.5, 10000)
        osc1 = OscillatorWithAmplitudeEnvelope(options, amp_env, freq)
        return [osc1]