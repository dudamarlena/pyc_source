# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/records/tests.py
# Compiled at: 2016-01-01 14:54:37
from binascii import hexlify
from datetime import datetime
from pprint import pformat
import json, difflib
from times import *
from bolus import *
_midnights = {'page_4': [
            bytearray([7, 0]) + bytearray([0, 5, 38, 7, 141]) + bytearray([109, 7, 141, 5, 0, 148, 88, 216,
             7, 0, 0, 5, 38, 3, 114, 67,
             1, 180, 33, 0, 121, 1, 180, 33,
             1, 100, 82, 0, 80, 18, 0, 0,
             0, 5, 4, 1, 0, 0, 12, 0,
             232, 0, 0, 0]),
            bytearray([7, 0]) + bytearray([0, 5, 116, 8, 141]) + bytearray([109, 8, 141, 5, 16, 246, 142, 143,
             5, 0, 0, 5, 116, 3, 116, 63,
             2, 0, 37, 0, 53, 2, 0, 37,
             0, 160, 31, 1, 96, 69, 0, 0,
             0, 4, 0, 3, 1, 0, 12, 0,
             232, 0, 0, 0]),
            bytearray([7, 0]) + bytearray([0, 4, 70, 9, 141]) + bytearray([109, 9, 141, 5, 16, 211, 98, 41,
             3, 0, 0, 4, 70, 3, 118, 81,
             0, 208, 19, 0, 44, 0, 208, 19,
             0, 124, 60, 0, 84, 40, 0, 0,
             0, 2, 1, 1, 0, 0, 12, 0,
             232, 0, 0, 0])], 
   'page_14': [
             bytearray([7, 0]) + bytearray([0, 6, 6, 194, 12]) + bytearray([109, 194, 12, 5, 16, 177, 96, 139,
              9, 0, 0, 6, 6, 3, 124, 58,
              2, 138, 42, 0, 100, 2, 138, 42,
              1, 46, 46, 1, 92, 54, 0, 0,
              0, 7, 3, 4, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 5, 12, 195, 12]) + bytearray([109, 195, 12, 5, 16, 183, 77, 20,
              3, 0, 0, 5, 12, 3, 124, 69,
              1, 144, 31, 0, 95, 1, 144, 31,
              1, 4, 65, 0, 140, 35, 0, 0,
              0, 4, 3, 1, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 5, 158, 196, 12]) + bytearray([109, 196, 12, 5, 0, 170, 137, 198,
              3, 0, 0, 5, 158, 3, 118, 62,
              2, 40, 38, 0, 143, 2, 40, 38,
              1, 176, 78, 0, 120, 22, 0, 0,
              0, 5, 3, 2, 0, 0, 12, 0,
              232, 0, 0, 0])], 
   'page_29': [
             bytearray([7, 0]) + bytearray([0, 5, 156, 168, 12]) + bytearray([109, 168, 12, 5, 16, 171, 97, 26,
              3, 0, 0, 5, 156, 3, 120, 62,
              2, 36, 38, 0, 139, 2, 36, 38,
              1, 156, 75, 0, 136, 25, 0, 0,
              0, 4, 3, 1, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 5, 114, 169, 12]) + bytearray([109, 169, 12, 5, 0, 150, 115, 182,
              3, 0, 0, 5, 114, 3, 118, 64,
              1, 252, 36, 0, 145, 1, 252, 36,
              1, 180, 86, 0, 72, 14, 0, 0,
              0, 7, 5, 2, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 4, 210, 170, 12]) + bytearray([109, 170, 12, 5, 16, 182, 141, 35,
              5, 0, 0, 4, 210, 3, 114, 71,
              1, 96, 29, 0, 54, 1, 96, 29,
              0, 160, 45, 0, 192, 55, 0, 0,
              0, 4, 2, 2, 0, 0, 12, 0,
              232, 0, 0, 0])], 
   'page_35': [
             bytearray([7, 0]) + bytearray([0, 4, 150, 141, 140]) + bytearray([109, 141, 140, 5, 0, 128, 104, 151,
              2, 0, 0, 4, 150, 3, 66, 71,
              1, 84, 29, 0, 109, 1, 84, 29,
              1, 64, 94, 0, 20, 6, 0, 0,
              0, 5, 4, 1, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 4, 224, 142, 140]) + bytearray([109, 142, 140, 5, 0, 116, 102, 142,
              7, 0, 0, 4, 224, 3, 116, 71,
              1, 108, 29, 0, 123, 1, 108, 29,
              1, 108, 100, 0, 0, 0, 0, 0,
              0, 5, 5, 0, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 4, 102, 143, 140]) + bytearray([109, 143, 140, 5, 0, 128, 66, 242,
              5, 0, 0, 4, 102, 3, 86, 76,
              1, 16, 24, 0, 91, 1, 16, 24,
              1, 16, 100, 0, 0, 0, 0, 0,
              0, 2, 2, 0, 0, 0, 12, 0,
              232, 0, 0, 0]),
             bytearray([7, 0]) + bytearray([0, 5, 32, 144, 140]) + bytearray([109, 144, 140, 5, 0, 137, 108, 170,
              3, 0, 0, 5, 32, 3, 120, 68,
              1, 168, 32, 0, 126, 1, 168, 32,
              1, 128, 91, 0, 40, 9, 0, 0,
              0, 5, 3, 1, 1, 0, 12, 0,
              232, 0, 0, 0])]}
_bewest_dates = {'page-19': {0: [
                 170, 247, 64, 12, 12], 
               1: [
                 64, 12, 12, 10, 12], 
               2: [
                 12, 139, 195, 40, 12], 
               3: [
                 139, 195, 40, 12, 140], 
               4: [
                 40, 12, 140, 91, 12], 
               5: [
                 141, 195, 8, 12, 12], 
               6: [
                 170, 247, 0, 12, 12]}}

def _test_decode_bolus():
    """
  ## correct
  >>> parse_date( bytearray( _bewest_dates['page-19'][6] ) ).isoformat( )
  '2012-11-12T00:55:42'

  ## correct
  >>> parse_date( bytearray( _bewest_dates['page-19'][0] ) ).isoformat( )
  '2012-11-12T00:55:42'

  ## this is wrong
  >>> parse_date( bytearray( _bewest_dates['page-19'][1] ) ).isoformat( )
  '2012-04-10T12:12:00'

  ## day,month is wrong, time H:M:S is correct
  # expected:
  >>> parse_date( bytearray( _bewest_dates['page-19'][2] ) ).isoformat( )
  '2012-02-08T03:11:12'

  ## correct
  >>> parse_date( bytearray( _bewest_dates['page-19'][3] ) ).isoformat( )
  '2012-11-12T08:03:11'

  #### not a valid date
  # >>> parse_date( bytearray( _bewest_dates['page-19'][4] ) ).isoformat( )

  ## correct
  >>> parse_date( bytearray( _bewest_dates['page-19'][5] ) ).isoformat( )
  '2012-11-12T08:03:13'

  """
    pass


_bad_days = [
 bytearray([169, 245, 21, 20, 12]),
 bytearray([166, 199, 54, 20, 140]),
 bytearray([169, 245, 21, 20, 12]),
 bytearray([166, 199, 54, 20, 140]),
 bytearray([162, 233, 16, 25, 12]),
 bytearray([160, 246, 13, 25, 12]),
 bytearray([165, 217, 52, 29, 12]),
 bytearray([194, 59, 14, 20, 12]),
 bytearray([217, 28, 15, 20, 12])]

def big_days(x=0):
    """
    # page 17, RECORD 11
    >>> parse_date( big_days(0) ).isoformat( )
    '2012-11-20T21:53:41'

    # page 17, ~ RECORD 12
    >>> parse_date( big_days(1) ).isoformat( )
    '2012-11-20T22:07:38'

    >>> parse_date( big_days(2) ).isoformat( )
    '2012-11-20T21:53:41'

    >>> parse_date( big_days(3) ).isoformat( )
    '2012-11-20T22:07:38'

    # page 16, RECORD ~15
    >>> parse_date( big_days(4) ).isoformat( )
    '2012-11-25T16:41:34'

    >>> parse_date( big_days(5) ).isoformat( )
    '2012-11-25T13:54:32'

    # page 15
    >>> parse_date( big_days(6) ).isoformat( )
    '2012-11-29T20:25:37'

    # page 0
    >>> parse_date( big_days(7) ).isoformat( )
    '2012-12-20T14:59:02'

    >>> parse_date( big_days(8) ).isoformat( )
    '2012-12-20T15:28:25'

  """
    return _bad_days[x]


_wizards = [
 bytearray([91, 75,
  15, 114, 21, 19, 13,
  87, 80, 13, 45, 106, 249, 66, 240,
  0, 0, 0, 59, 125]),
 bytearray([91, 83,
  0, 100, 22, 14, 13,
  94, 80, 13, 45, 106, 251, 72, 240,
  0, 10, 0, 67, 125])]
from decocare import models
model522 = models.PumpModel('522', None)

def _test_bolus_wizards():
    """
  >>> rec = BolusWizard( _wizards[0][:2], model522 )
  >>> print pformat(rec.parse( _wizards[0] ))
  {'_byte[5]': 249,
   '_byte[7]': 240,
   'bg': 75,
   'bg_target_high': 125,
   'bg_target_low': 106,
   'bolus_estimate': 5.9,
   'carb_input': 87,
   'carb_ratio': 13,
   'correction_estimate': -0.7,
   'food_estimate': 6.6,
   'sensitivity': 45,
   'unabsorbed_insulin_count': '??',
   'unabsorbed_insulin_total': 0.0,
   'unknown_byte[10]': 0,
   'unknown_byte[8]': 0}
  >>> print str(rec)
  BolusWizard 2013-01-19T21:50:15 head[2], body[13] op[0x5b]

  >>> rec = BolusWizard( _wizards[1][:2], model522 )
  >>> print pformat(rec.parse( _wizards[1] ))
  {'_byte[5]': 251,
   '_byte[7]': 240,
   'bg': 83,
   'bg_target_high': 125,
   'bg_target_low': 106,
   'bolus_estimate': 6.7,
   'carb_input': 94,
   'carb_ratio': 13,
   'correction_estimate': -0.5,
   'food_estimate': 7.2,
   'sensitivity': 45,
   'unabsorbed_insulin_count': '??',
   'unabsorbed_insulin_total': 1.0,
   'unknown_byte[10]': 0,
   'unknown_byte[8]': 0}

  >>> print str(rec)
  BolusWizard 2013-01-14T22:36:00 head[2], body[13] op[0x5b]

  """
    pass


_bolus = [
 bytearray([1, 26, 26, 0,
  15, 114, 149, 19, 13]),
 bytearray([1, 17, 17, 0,
  16, 121, 79, 15, 13])]

def _test_bolus():
    """
  >>> rec = Bolus( _bolus[0][:2] )
  >>> print pformat(rec.parse( _bolus[0] ))
  {'amount': 2.6, 'duration': 0, 'programmed': 2.6, 'type': 'normal'}

  >>> print str(rec)
  Bolus 2013-01-19T21:50:15 head[4], body[0] op[0x01]

  >>> rec = Bolus( _bolus[1][:2] )
  >>> print pformat(rec.parse( _bolus[1] ))
  {'amount': 1.7, 'duration': 0, 'programmed': 1.7, 'type': 'normal'}
  >>> print str(rec)
  Bolus 2013-01-15T15:57:16 head[4], body[0] op[0x01]

  """
    pass


class TestSaraBolus:
    hexdump = '\n  5b 67\n    a1 51 0e 04 0d\n    0d 50 00 78\n  3c 64 00 00 28 00 00 14 00 28 78\n  5c 08 44 79 c0 3c 4b d0\n  01 00 28 00 28 00 14 00\n    a1 51 4e 04 0d\n  0a fc\n    b4 54 2f 04 0d\n  5b fc\n    b7 54 0f 04 0d\n    00 50 00 78\n  3c 64 58 00 00 00 00 1c 00 3c 78\n  5c 0b 28 40 c0 44 b8 c0 3c 8a d0\n  01 00 3c 00 3c 00 1c 00\n    b7 54 4f 04 0d\n  '
    csv_breakdown = '\n  9/4/13 14:17:33,,,,,,,Normal,1.0,1.0,,,,,,,,,,,,,,,,,,,,,BolusNormal\n    "AMOUNT=1\n      CONCENTRATION=null\n      PROGRAMMED_AMOUNT=1\n      ACTION_REQUESTOR=pump\n      ENABLE=true\n      IS_DUAL_COMPONENT=false\n      UNABSORBED_INSULIN_TOTAL=0.5"\n    11345487207,52554138,86,Paradigm Revel - 723\n\n  9/4/13 14:17:33,,,,,,,,,,,,,,,1.0,120,100,12,60,13,103,0,1,0.5,,,,,,BolusWizardBolusEstimate,"BG_INPUT=103\n      BG_UNITS=mg dl\n      CARB_INPUT=13\n      CARB_UNITS=grams\n      CARB_RATIO=12\n      INSULIN_SENSITIVITY=60\n      BG_TARGET_LOW=100\n      BG_TARGET_HIGH=120\n      BOLUS_ESTIMATE=1\n      CORRECTION_ESTIMATE=0\n      FOOD_ESTIMATE=1\n      UNABSORBED_INSULIN_TOTAL=0.5\n      UNABSORBED_INSULIN_COUNT=2\n      ACTION_REQUESTOR=pump"\n    11345487208,52554138,87,Paradigm Revel - 723\n\n  9/4/13 14:17:33,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,UnabsorbedInsulin,"BOLUS_ESTIMATE_DATUM=11345487208\n      INDEX=0\n      AMOUNT=1.7\n      RECORD_AGE=121\n      INSULIN_TYPE=null\n      INSULIN_ACTION_CURVE=180"\n    11345487209,52554138,88,Paradigm Revel - 723\n\n  9/4/13 14:17:33,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,UnabsorbedInsulin,"BOLUS_ESTIMATE_DATUM=11345487208\n      INDEX=1\n      AMOUNT=1.5\n      RECORD_AGE=331\n      INSULIN_TYPE=null\n      INSULIN_ACTION_CURVE=180"\n    11345487210,52554138,89,Paradigm Revel - 723\n\n  9/4/13 15:20:52,,,,,,,,,,,,,,,,,,,,,,,,,,252,,,,CalBGForPH,"AMOUNT=252, ACTION_REQUESTOR=pump"\n    11345487206,52554138,85,Paradigm Revel - 723\n\n  9/4/13 15:20:55,,,,,,,Normal,1.5,1.5,,,,,,,,,,,,,,,,,,,,,BolusNormal,"AMOUNT=1.5\n      CONCENTRATION=null\n      PROGRAMMED_AMOUNT=1.5\n      ACTION_REQUESTOR=pump\n      ENABLE=true\n      IS_DUAL_COMPONENT=false\n      UNABSORBED_INSULIN_TOTAL=0.7"\n    11345487201,52554138,80,Paradigm Revel - 723\n\n  9/4/13 15:20:55,,,,,,,,,,,,,,,1.5,120,100,12,60,0,252,2.2,0,0.7,,,,,,BolusWizardBolusEstimate,"BG_INPUT=252\n      BG_UNITS=mg dl\n      CARB_INPUT=0\n      CARB_UNITS=grams\n      CARB_RATIO=12\n      INSULIN_SENSITIVITY=60\n      BG_TARGET_LOW=100\n      BG_TARGET_HIGH=120\n      BOLUS_ESTIMATE=1.5\n      CORRECTION_ESTIMATE=2.2\n      FOOD_ESTIMATE=0\n      UNABSORBED_INSULIN_TOTAL=0.7\n      UNABSORBED_INSULIN_COUNT=3\n      ACTION_REQUESTOR=pump"\n    11345487202,52554138,81,Paradigm Revel - 723\n\n  9/4/13 15:20:55,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,UnabsorbedInsulin,"BOLUS_ESTIMATE_DATUM=11345487202\n      INDEX=0\n      AMOUNT=1\n      RECORD_AGE=64\n      INSULIN_TYPE=null\n      INSULIN_ACTION_CURVE=180"\n    11345487203,52554138,82,Paradigm Revel - 723\n\n  9/4/13 15:20:55,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,UnabsorbedInsulin,"BOLUS_ESTIMATE_DATUM=11345487202\n      INDEX=1\n      AMOUNT=1.7\n      RECORD_AGE=184\n      INSULIN_TYPE=null\n      INSULIN_ACTION_CURVE=180"\n    11345487204,52554138,83,Paradigm Revel - 723\n\n  9/4/13 15:20:55,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,UnabsorbedInsulin,"BOLUS_ESTIMATE_DATUM=11345487202\n      INDEX=2\n      AMOUNT=1.5\n      RECORD_AGE=394\n      INSULIN_TYPE=null\n      INSULIN_ACTION_CURVE=180"\n    11345487205,52554138,84,Paradigm Revel - 723\n  9/4/13 16:11:57,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,CurrentSensorMissedDataTime,TIME=1800000,11345487185,52554138,64,Paradigm Revel - 723\n  '
    bolus_1_ok = {'bg': 103, 
       'carb_input': 13, 
       'carb_ratio': 12, 
       'sensitivity': 60, 
       'bg_target_low': 100, 
       'bg_target_high': 120, 
       'bolus_estimate': 1, 
       'correction_estimate': 0, 
       'food_estimate': 1, 
       'unabsorbed_insulin_total': 0.5, 
       'unabsorbed_insulin_count': 2}
    bw_1_bytes = bytearray(('').join(('\n  5b 67\n    a1 51 0e 04 0d\n    0d 50 00 78\n    3c 64 00 00 28 00 00 14 00 28 78\n  ').strip().split()).decode('hex'))
    bw_2_bytes = bytearray(('').join(('\n  5b fc\n    b7 54 0f 04 0d\n    00 50 00 78\n    3c 64 58 00 00 00 00 1c 00 3c 78\n  ').strip().split()).decode('hex'))
    cal_bg_bytes = bytearray(('').join(('\n  0a fc\n    b4 54 2f 04 0d\n  ').strip().split()).decode('hex'))

    @classmethod
    def test_cal_bg(klass):
        """
    >>> TestSaraBolus.test_cal_bg( )
    CalBGForPH 2013-09-04T15:20:52 head[2], body[0] op[0x0a]
    {
      "amount": 252
    }
    """
        data = klass.cal_bg_bytes
        rec = CalBGForPH(data[:2])
        d = rec.parse(data)
        print str(rec)
        print json.dumps(d, indent=2)


def dictlines(d):
    items = d.items()
    items.sort()
    d = [ '%s: %s\n' % (k, v) for k, v in items ]
    return d


def unsolved_bolus_wizard():
    """
  # >>> unsolved_bolus_wizard( )
  """
    bw_ok_1 = {'bg_input': 103, 
       'carb_input': 13, 
       'carb_ratio': 12, 
       'insulin_sensitivity': 60, 
       'bg_target_low': 100, 
       'bg_target_high': 120, 
       'bolus_estimate': 1, 
       'correction_estimate': 0, 
       'food_estimate': 1, 
       'unabsorbed_insulin_total': 0.5, 
       'unabsorbed_insulin_count': 2}
    bw_ok_2 = {'bg_input': 252, 
       'carb_input': 0, 
       'carb_ratio': 12, 
       'insulin_sensitivity': 60, 
       'bg_target_low': 100, 
       'bg_target_high': 120, 
       'bolus_estimate': 1.5, 
       'correction_estimate': 2.2, 
       'food_estimate': 0, 
       'unabsorbed_insulin_total': 0.7, 
       'unabsorbed_insulin_count': 3}
    found = decode_wizard(TestSaraBolus.bw_1_bytes)
    if found != bw_ok_1:
        print 'FOUND:'
        print json.dumps(found, indent=2)
        print 'EXPECTED:'
        print json.dumps(bw_ok_1, indent=2)
    found = decode_wizard(TestSaraBolus.bw_2_bytes)
    if found != bw_ok_2:
        print 'FOUND:'
        print json.dumps(found, indent=2)
        print 'EXPECTED:'
        print json.dumps(bw_ok_2, indent=2)


def decode_wizard(data):
    """
  BYTE
  01:
  02:
  03:
  04:
  05:
  06:
  07:
  08:
  09:
  10:
  12:
  13:
  14:
  15:
  16:
  17:
  18:
  19:
  20:
  21:
  22:
  """
    head = data[:2]
    date = data[2:7]
    datetime = parse_date(date)
    body = data[7:]
    bg = lib.BangInt([body[1] & 15, head[1]])
    carb_input = int(body[0])
    carb_ratio = int(body[2])
    bg_target_low = int(body[5])
    bg_target_high = int(body[3])
    sensitivity = int(body[4])
    print 'BOLUS WIZARD', datetime.isoformat()
    wizard = {'bg_input': bg, 'carb_input': carb_input, 'carb_ratio': carb_ratio, 
       'insulin_sensitivity': sensitivity, 
       'bg_target_low': bg_target_low, 
       'bg_target_high': bg_target_high}
    return wizard


class BW722(BolusWizard):

    def decode(self):
        self.parse_time()
        bg = lib.BangInt([self.body[1] & 15, self.head[1]])
        carb_input = int(self.body[0])
        carb_ratio = int(self.body[2])
        bg_target_low = int(self.body[5])
        bg_target_high = int(self.body[3])
        sensitivity = int(self.body[12])
        correction = (twos_comp(self.body[7], 8) + twos_comp(self.body[5] & 15, 8)) / 10.0
        wizard = {'bg': bg, 'carb_input': carb_input, 'carb_ratio': carb_ratio, 
           'sensitivity': sensitivity, 
           'bg_target_low': bg_target_low, 
           'bg_target_high': bg_target_high, 
           'correction_estimate': correction}
        return wizard


if __name__ == '__main__':
    import doctest
    doctest.testmod()