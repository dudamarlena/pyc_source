# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/midi.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2898 bytes
import fractions
from . import control
from ..util import log
try:
    import mido
    MESSAGE_TYPES = set(s['type'] for s in mido.messages.specs.SPECS)
except:
    mido = None
    MESSAGE_TYPES = set()

MIDO_ERROR = 'You need to install mido.  Try\n    pip install mido\n'
MIDO_BACKEND_ERROR = 'You have the wrong rtmidi installed.  Try\n    pip uninstall -y rtmidi\n    pip install -y python-rtmidi\n'

class Midi(control.ExtractedLoop):
    EXTRACTOR = {'keys_by_type':{'aftertouch':('port', 'channel', 'type', 'value'), 
      'control_change':('port', 'channel', 'type', 'control', 'value'), 
      'note_off':('port', 'channel', 'type', 'note', 'velocity'), 
      'note_on':('port', 'channel', 'type', 'note', 'velocity'), 
      'pitchwheel':('port', 'channel', 'type', 'pitch'), 
      'program_change':('port', 'channel', 'type', 'program')}, 
     'normalizers':{'pitch':lambda x: fractions.Fraction(x - 8192) / 8192, 
      'value':lambda x: fractions.Fraction(x) / 127, 
      'velocity':lambda x: fractions.Fraction(x) / 127}, 
     'omit':('port', 'channel')}

    def __init__(self, use_note_off=True, **kwds):
        """
        :param use_note_off:
            If False, map note_offs to note_ons with velocity 0
            If True, map note_ons with velocity 0 to note_offs
            If None, do not change none_ons or note_offs
        """
        (super().__init__)(**kwds)
        self.use_note_off = use_note_off

    def messages(self):
        if not mido:
            raise ValueError(MIDO_ERROR)
        try:
            input_names = mido.get_input_names()
        except AttributeError as e:
            e.args = (
             MIDO_ERROR,) + e.args
            raise

        ports = [mido.open_input(i) for i in input_names]
        if not ports:
            log.error('control.midi: no MIDI ports found')
            return
        port_names = ', '.join('"%s"' % p.name for p in ports)
        log.info('Starting to listen for MIDI on port%s %s', '' if len(ports) == 1 else 's', port_names)
        for port, msg in mido.ports.MultiPort(ports, yield_ports=True):
            mdict = dict((vars(msg)), port=port)
            if self.use_note_off:
                if msg.type == 'note_on':
                    if not msg.velocity:
                        mdict.update(type='note_off')
            else:
                if self.use_note_off is False:
                    if msg.type == 'note_off':
                        mdict.update(type='note_on', velocity=0)
                yield mdict