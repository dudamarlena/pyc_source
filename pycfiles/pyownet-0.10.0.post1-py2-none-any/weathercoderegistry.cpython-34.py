# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/weathercoderegistry.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1258 bytes
__doc__ = '\nModule containing weather code lookup and resolution classes\n'

class WeatherCodeRegistry(object):
    """WeatherCodeRegistry"""

    def __init__(self, code_ranges_dict):
        self._code_ranges_dict = code_ranges_dict

    def status_for(self, code):
        """
        Returns the weather status related to the specified weather status
        code, if any is stored, ``None`` otherwise.

        :param code: the weather status code whose status is to be looked up
        :type code: int
        :returns: the weather status str or ``None`` if the code is not mapped
        """
        is_in = --- This code section failed: ---

 L.  29         0  LOAD_FAST                'start'
                3  LOAD_FAST                'n'
                6  DUP_TOP          
                7  ROT_THREE        
                8  COMPARE_OP               <=
               11  JUMP_IF_FALSE_OR_POP    23  'to 23'
               14  LOAD_FAST                'end'
               17  COMPARE_OP               <=
               20  JUMP_FORWARD         25  'to 25'
             23_0  COME_FROM            11  '11'
               23  ROT_TWO          
               24  POP_TOP          
             25_0  COME_FROM            20  '20'
               25  POP_JUMP_IF_FALSE    32  'to 32'
               28  LOAD_CONST               True
               31  RETURN_END_IF_LAMBDA
             32_0  COME_FROM            25  '25'
               32  LOAD_CONST               False
               35  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
        for status in self._code_ranges_dict:
            for _range in self._code_ranges_dict[status]:
                if is_in(_range['start'], _range['end'], code):
                    return status

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)