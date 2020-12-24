# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/records/bolus.py
# Compiled at: 2016-10-26 17:37:08
from base import KnownRecord, VariableHead
from decocare import lib
from times import extra_year_bits
from pprint import pformat

class Bolus(KnownRecord):
    """
  >>> rec = Bolus(Bolus._test_1[:4])
  >>> decoded = rec.parse(Bolus._test_1)
  >>> print str(rec)
  Bolus 2012-12-18T15:05:28 head[4], body[0] op[0x01]

  >>> print pformat(decoded)
  {'amount': 5.6, 'duration': 0, 'programmed': 5.6, 'type': 'normal'}

  """
    _test_1 = bytearray([1, 56, 56, 0,
     220, 5, 79, 18, 12])
    opcode = 1
    head_length = 4

    def __init__(self, head, larger=False):
        super(Bolus, self).__init__(head, larger)
        if self.larger:
            self.head_length = 8

    def decode(self):
        self.parse_time()
        dose = {'amount': self.head[2] / 10.0, 
           'programmed': self.head[1] / 10.0, 
           'duration': self.head[3] * 30, 
           'type': self.head[3] > 0 and 'square' or 'normal'}
        if self.larger:
            duration = self.head[7] * 30
            dose = {'amount': lib.BangInt(self.head[3:5]) / 40.0, 'programmed': lib.BangInt(self.head[1:3]) / 40.0, 
               'unabsorbed': lib.BangInt(self.head[5:7]) / 40.0, 
               'duration': duration, 
               'type': duration > 0 and 'square' or 'normal'}
        return dose


class BolusWizard(KnownRecord):
    """
  Decode/parse bolus wizard records.

  >>> from decocare import models
  >>> rec = BolusWizard(BolusWizard._test_1[:2], model=models.PumpModel('522', None))
  >>> decoded = rec.parse(BolusWizard._test_1)
  >>> print str(rec)
  BolusWizard 2013-01-20T13:07:45 head[2], body[13] op[0x5b]

  >>> print pformat(decoded)
  {'_byte[5]': 0,
   '_byte[7]': 0,
   'bg': 108,
   'bg_target_high': 125,
   'bg_target_low': 106,
   'bolus_estimate': 1.1,
   'carb_input': 15,
   'carb_ratio': 13,
   'correction_estimate': 0.0,
   'food_estimate': 1.1,
   'sensitivity': 45,
   'unabsorbed_insulin_count': '??',
   'unabsorbed_insulin_total': 4.8,
   'unknown_byte[10]': 0,
   'unknown_byte[8]': 0}

  """
    _test_1 = bytearray([91, 108,
     45, 71, 13, 20, 13,
     15, 80, 13, 45, 106, 0, 11, 0,
     0, 48, 0, 11, 125])
    _test_2 = bytearray([91, 139,
     220, 5, 15, 18, 12,
     69, 80, 13, 45, 106, 3, 53, 0,
     0, 0, 0, 56, 125])
    opcode = 91
    body_length = 13

    def __init__(self, head, model=None):
        super(BolusWizard, self).__init__(head, model)
        self.MMOL_DEFAULT = model.MMOL_DEFAULT
        if self.larger:
            self.body_length = 15

    def decode(self):
        self.parse_time()
        bg = lib.BangInt([self.body[1] & 15, self.head[1]])
        carb_input = int(self.body[0])
        correction = (twos_comp(self.body[7], 8) + twos_comp(self.body[5] & 15, 8)) / 10.0
        wizard = {'bg': bg, 'carb_input': carb_input, 'carb_ratio': int(self.body[2]), 
           'sensitivity': int(self.body[3]), 
           'bg_target_low': int(self.body[4]), 
           'bg_target_high': int(self.body[12]), 
           'bolus_estimate': int(self.body[11]) / 10.0, 
           'food_estimate': int(self.body[6]) / 10.0, 
           'unabsorbed_insulin_total': int(self.body[9]) / 10.0, 
           'unabsorbed_insulin_count': '??', 
           'correction_estimate': correction, 
           '_byte[5]': self.body[5], 
           '_byte[7]': int(self.body[7]), 
           'unknown_byte[8]': self.body[8], 
           'unknown_byte[10]': self.body[10]}
        if self.larger:
            bg = ((self.body[1] & 3) << 8) + self.head[1]
            carb_input = ((self.body[1] & 12) << 6) + self.body[0]
            carb_ratio = (((self.body[2] & 7) << 8) + self.body[3]) / 10.0
            sensitivity = int(self.body[4])
            wizard = {'bg': bg, 'carb_input': carb_input, 'carb_ratio': carb_ratio, 
               'sensitivity': sensitivity, 
               'bg_target_low': int(self.body[5]), 
               'bg_target_high': int(self.body[14]), 
               'correction_estimate': (((self.body[9] & 56) << 5) + self.body[6]) / 40.0, 
               'food_estimate': insulin_decode(self.body[7], self.body[8]), 
               'unabsorbed_insulin_total': insulin_decode(self.body[10], self.body[11]), 
               'bolus_estimate': insulin_decode(self.body[12], self.body[13])}
        if self.MMOL_DEFAULT:
            for key in ['bg', 'bg_target_high', 'bg_target_low', 'sensitivity']:
                wizard[key] = wizard[key] / 10.0

        return wizard


def insulin_decode(a, b, strokes=40.0):
    return ((a << 8) + b) / strokes


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if val & 1 << bits - 1 != 0:
        val = val - (1 << bits)
    return val


class UnabsorbedInsulinBolus(VariableHead):
    """
  This data is not made available at the time of therapy in the pump
  UI, but could easily change my dosing decision.

  >>> from decocare import models
  >>> model = models.PumpModel('522', None)
  >>> rec = UnabsorbedInsulinBolus( UnabsorbedInsulinBolus._test_1[:2], model)
  >>> print str(rec)
  UnabsorbedInsulinBolus unknown head[2], body[0] op[0x5c]

  >>> print pformat(rec.parse( UnabsorbedInsulinBolus._test_1 ))
  [{'age': 78, 'amount': 1.25}, {'age': 88, 'amount': 0.95}]

  >>> rec = UnabsorbedInsulinBolus( UnabsorbedInsulinBolus._test_2[:2], model )
  >>> print str(rec)
  UnabsorbedInsulinBolus unknown head[2], body[0] op[0x5c]

  >>> print pformat(rec.parse( UnabsorbedInsulinBolus._test_2 ))
  [{'age': 60, 'amount': 2.6}, {'age': 160, 'amount': 2.5}]

  [{'age': 60, 'amount': 2.6, 'curve': 4},
   {'age': 160, 'amount': 2.5, 'curve': 4}]

  """
    _test_1 = bytearray([92, 8,
     50, 78, 4, 38, 88, 4])
    _test_2 = bytearray([92, 8,
     104, 60, 4,
     100, 160, 4])
    opcode = 92
    date_length = 0

    def decode(self):
        raw = self.head[2:]
        return self.model.decode_unabsorbed(raw)


class CalBGForPH(KnownRecord):
    """
    >>> rec = CalBGForPH( CalBGForPH._test_1[:2] )
    >>> rec.parse( CalBGForPH._test_1 )
    {'amount': 139}
    >>> print str(rec)
    CalBGForPH 2012-12-18T15:04:46 head[2], body[0] op[0x0a]

  """
    _test_1 = bytearray([10, 139,
     238, 4, 47, 18, 12])
    _test_2 = bytearray([10, 167,
     34, 83, 48, 14, 13])
    _test_3 = bytearray([10, 176,
     0, 111, 47, 14, 13])
    _test_4 = bytearray([10, 66,
     12, 108, 49, 14, 141])
    _test_5 = bytearray([10, 96,
     4, 89, 43, 14, 141])
    _test_6 = bytearray([10, 91,
     22, 82, 42, 14, 141])
    opcode = 10

    def decode(self):
        self.parse_time()
        highbit = (self.date[2] & 128) << 2
        nibble = (self.date[4] & 128) << 1
        low = self.head[1]
        amount = int(highbit + nibble + low)
        return {'amount': amount}


if __name__ == '__main__':
    import doctest
    doctest.testmod()