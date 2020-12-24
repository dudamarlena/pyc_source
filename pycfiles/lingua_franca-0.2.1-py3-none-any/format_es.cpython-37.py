# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/lang/format_es.py
# Compiled at: 2020-03-04 07:40:03
# Size of source mod 2**32: 10017 bytes
"""
Format functions for castillian (es-es)

"""
from lingua_franca.lang.format_common import convert_to_mixed_fraction
NUM_STRING_ES = {0:'cero', 
 1:'uno', 
 2:'dos', 
 3:'tres', 
 4:'cuatro', 
 5:'cinco', 
 6:'seis', 
 7:'siete', 
 8:'ocho', 
 9:'nueve', 
 10:'diez', 
 11:'once', 
 12:'doce', 
 13:'trece', 
 14:'catorce', 
 15:'quince', 
 16:'dieciséis', 
 17:'diecisete', 
 18:'dieciocho', 
 19:'diecinueve', 
 20:'veinte', 
 30:'treinta', 
 40:'cuarenta', 
 50:'cincuenta', 
 60:'sesenta', 
 70:'setenta', 
 80:'ochenta', 
 90:'noventa'}
FRACTION_STRING_ES = {2:'medio', 
 3:'tercio', 
 4:'cuarto', 
 5:'quinto', 
 6:'sexto', 
 7:'séptimo', 
 8:'octavo', 
 9:'noveno', 
 10:'décimo', 
 11:'onceavo', 
 12:'doceavo', 
 13:'treceavo', 
 14:'catorceavo', 
 15:'quinceavo', 
 16:'dieciseisavo', 
 17:'diecisieteavo', 
 18:'dieciochoavo', 
 19:'diecinueveavo', 
 20:'veinteavo'}

def nice_number_es(number, speech, denominators=range(1, 21)):
    """ Spanish helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 y medio" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    strNumber = ''
    whole = 0
    num = 0
    den = 0
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        whole = round(number, 3)
    else:
        whole, num, den = result
    if not speech:
        if num == 0:
            strNumber = '{:,}'.format(whole)
            strNumber = strNumber.replace(',', '\xa0')
            strNumber = strNumber.replace('.', ',')
            return strNumber
        return '{} {}/{}'.format(whole, num, den)
    else:
        if num == 0:
            strNumber = str(whole)
            strNumber = strNumber.replace('.', ',')
            return strNumber
        den_str = FRACTION_STRING_ES[den]
        if whole == 0:
            if num == 1:
                strNumber = 'un {}'.format(den_str)
            else:
                strNumber = '{} {}'.format(num, den_str)
        else:
            if num == 1:
                if den == 2:
                    strNumber = '{} y {}'.format(whole, den_str)
                else:
                    strNumber = '{} y 1 {}'.format(whole, den_str)
            else:
                strNumber = '{} y {} {}'.format(whole, num, den_str)
        if num > 1:
            if den != 3:
                strNumber += 's'
        return strNumber


def pronounce_number_es(num, places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'cinco coma dos'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    if abs(num) >= 100:
        return str(num)
        result = ''
        if num < 0:
            result = 'menos '
        else:
            num = abs(num)
            if 20 <= num <= 29:
                tens = int(num - int(num) % 10)
                ones = int(num - tens)
                result += NUM_STRING_ES[tens]
                if ones > 0:
                    result = result[:-1]
                    if ones == 2:
                        result += 'idós'
            elif ones == 3:
                result += 'itrés'
            else:
                if ones == 6:
                    result += 'iséis'
                else:
                    result += 'i' + NUM_STRING_ES[ones]
    else:
        if num >= 30:
            tens = int(num - int(num) % 10)
            ones = int(num - tens)
            result += NUM_STRING_ES[tens]
            if ones > 0:
                result += ' y ' + NUM_STRING_ES[ones]
            else:
                result += NUM_STRING_ES[int(num)]
        elif not num == int(num):
            if places > 0:
                if abs(num) < 1.0:
                    result is 'menos ' or result or result += 'cero'
                result += ' coma'
                _num_str = str(num)
                _num_str = _num_str.split('.')[1][0:places]
                for char in _num_str:
                    result += ' ' + NUM_STRING_ES[int(char)]

        return result


def nice_time_es--- This code section failed: ---

 L. 222         0  LOAD_FAST                'use_24hour'
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L. 224         4  LOAD_FAST                'dt'
                6  LOAD_METHOD              strftime
                8  LOAD_STR                 '%H:%M'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'string'
               14  JUMP_FORWARD         66  'to 66'
             16_0  COME_FROM             2  '2'

 L. 226        16  LOAD_FAST                'use_ampm'
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 228        20  LOAD_FAST                'dt'
               22  LOAD_METHOD              strftime
               24  LOAD_STR                 '%I:%M %p'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  STORE_FAST               'string'
               30  JUMP_FORWARD         42  'to 42'
             32_0  COME_FROM            18  '18'

 L. 231        32  LOAD_FAST                'dt'
               34  LOAD_METHOD              strftime
               36  LOAD_STR                 '%I:%M'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  STORE_FAST               'string'
             42_0  COME_FROM            30  '30'

 L. 232        42  LOAD_FAST                'string'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '0'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    66  'to 66'

 L. 233        54  LOAD_FAST                'string'
               56  LOAD_CONST               1
               58  LOAD_CONST               None
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  STORE_FAST               'string'
             66_0  COME_FROM            52  '52'
             66_1  COME_FROM            14  '14'

 L. 235        66  LOAD_FAST                'speech'
               68  POP_JUMP_IF_TRUE     74  'to 74'

 L. 236        70  LOAD_FAST                'string'
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'

 L. 239        74  LOAD_STR                 ''
               76  STORE_FAST               'speak'

 L. 240        78  LOAD_FAST                'use_24hour'
               80  POP_JUMP_IF_FALSE   172  'to 172'

 L. 245        82  LOAD_FAST                'dt'
               84  LOAD_ATTR                hour
               86  LOAD_CONST               1
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   102  'to 102'

 L. 246        92  LOAD_FAST                'speak'
               94  LOAD_STR                 'la una'
               96  INPLACE_ADD      
               98  STORE_FAST               'speak'
              100  JUMP_FORWARD        120  'to 120'
            102_0  COME_FROM            90  '90'

 L. 248       102  LOAD_FAST                'speak'
              104  LOAD_STR                 'las '
              106  LOAD_GLOBAL              pronounce_number_es
              108  LOAD_FAST                'dt'
              110  LOAD_ATTR                hour
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  BINARY_ADD       
              116  INPLACE_ADD      
              118  STORE_FAST               'speak'
            120_0  COME_FROM           100  '100'

 L. 251       120  LOAD_FAST                'dt'
              122  LOAD_ATTR                minute
              124  LOAD_CONST               10
              126  COMPARE_OP               <
              128  POP_JUMP_IF_FALSE   150  'to 150'

 L. 252       130  LOAD_FAST                'speak'
              132  LOAD_STR                 ' cero '
              134  LOAD_GLOBAL              pronounce_number_es
              136  LOAD_FAST                'dt'
              138  LOAD_ATTR                minute
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  BINARY_ADD       
              144  INPLACE_ADD      
              146  STORE_FAST               'speak'
              148  JUMP_FORWARD        660  'to 660'
            150_0  COME_FROM           128  '128'

 L. 254       150  LOAD_FAST                'speak'
              152  LOAD_STR                 ' '
              154  LOAD_GLOBAL              pronounce_number_es
              156  LOAD_FAST                'dt'
              158  LOAD_ATTR                minute
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  BINARY_ADD       
              164  INPLACE_ADD      
              166  STORE_FAST               'speak'
          168_170  JUMP_FORWARD        660  'to 660'
            172_0  COME_FROM            80  '80'

 L. 258       172  LOAD_FAST                'dt'
              174  LOAD_ATTR                minute
              176  LOAD_CONST               35
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   198  'to 198'

 L. 259       182  LOAD_CONST               -25
              184  STORE_FAST               'minute'

 L. 260       186  LOAD_FAST                'dt'
              188  LOAD_ATTR                hour
              190  LOAD_CONST               1
              192  BINARY_ADD       
              194  STORE_FAST               'hour'
              196  JUMP_FORWARD        318  'to 318'
            198_0  COME_FROM           180  '180'

 L. 261       198  LOAD_FAST                'dt'
              200  LOAD_ATTR                minute
              202  LOAD_CONST               40
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 262       208  LOAD_CONST               -20
              210  STORE_FAST               'minute'

 L. 263       212  LOAD_FAST                'dt'
              214  LOAD_ATTR                hour
              216  LOAD_CONST               1
              218  BINARY_ADD       
              220  STORE_FAST               'hour'
              222  JUMP_FORWARD        318  'to 318'
            224_0  COME_FROM           206  '206'

 L. 264       224  LOAD_FAST                'dt'
              226  LOAD_ATTR                minute
              228  LOAD_CONST               45
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   250  'to 250'

 L. 265       234  LOAD_CONST               -15
              236  STORE_FAST               'minute'

 L. 266       238  LOAD_FAST                'dt'
              240  LOAD_ATTR                hour
              242  LOAD_CONST               1
              244  BINARY_ADD       
              246  STORE_FAST               'hour'
              248  JUMP_FORWARD        318  'to 318'
            250_0  COME_FROM           232  '232'

 L. 267       250  LOAD_FAST                'dt'
              252  LOAD_ATTR                minute
              254  LOAD_CONST               50
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   278  'to 278'

 L. 268       262  LOAD_CONST               -10
              264  STORE_FAST               'minute'

 L. 269       266  LOAD_FAST                'dt'
              268  LOAD_ATTR                hour
              270  LOAD_CONST               1
              272  BINARY_ADD       
              274  STORE_FAST               'hour'
              276  JUMP_FORWARD        318  'to 318'
            278_0  COME_FROM           258  '258'

 L. 270       278  LOAD_FAST                'dt'
              280  LOAD_ATTR                minute
              282  LOAD_CONST               55
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   306  'to 306'

 L. 271       290  LOAD_CONST               -5
              292  STORE_FAST               'minute'

 L. 272       294  LOAD_FAST                'dt'
              296  LOAD_ATTR                hour
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               'hour'
              304  JUMP_FORWARD        318  'to 318'
            306_0  COME_FROM           286  '286'

 L. 274       306  LOAD_FAST                'dt'
              308  LOAD_ATTR                minute
              310  STORE_FAST               'minute'

 L. 275       312  LOAD_FAST                'dt'
              314  LOAD_ATTR                hour
              316  STORE_FAST               'hour'
            318_0  COME_FROM           304  '304'
            318_1  COME_FROM           276  '276'
            318_2  COME_FROM           248  '248'
            318_3  COME_FROM           222  '222'
            318_4  COME_FROM           196  '196'

 L. 277       318  LOAD_FAST                'hour'
              320  LOAD_CONST               0
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_TRUE    338  'to 338'
              328  LOAD_FAST                'hour'
              330  LOAD_CONST               12
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   348  'to 348'
            338_0  COME_FROM           324  '324'

 L. 278       338  LOAD_FAST                'speak'
              340  LOAD_STR                 'las doce'
              342  INPLACE_ADD      
              344  STORE_FAST               'speak'
              346  JUMP_FORWARD        418  'to 418'
            348_0  COME_FROM           334  '334'

 L. 279       348  LOAD_FAST                'hour'
              350  LOAD_CONST               1
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_TRUE    368  'to 368'
              358  LOAD_FAST                'hour'
              360  LOAD_CONST               13
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   378  'to 378'
            368_0  COME_FROM           354  '354'

 L. 280       368  LOAD_FAST                'speak'
              370  LOAD_STR                 'la una'
              372  INPLACE_ADD      
              374  STORE_FAST               'speak'
              376  JUMP_FORWARD        418  'to 418'
            378_0  COME_FROM           364  '364'

 L. 281       378  LOAD_FAST                'hour'
              380  LOAD_CONST               13
              382  COMPARE_OP               <
          384_386  POP_JUMP_IF_FALSE   402  'to 402'

 L. 282       388  LOAD_STR                 'las '
              390  LOAD_GLOBAL              pronounce_number_es
              392  LOAD_FAST                'hour'
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  BINARY_ADD       
              398  STORE_FAST               'speak'
              400  JUMP_FORWARD        418  'to 418'
            402_0  COME_FROM           384  '384'

 L. 284       402  LOAD_STR                 'las '
              404  LOAD_GLOBAL              pronounce_number_es
              406  LOAD_FAST                'hour'
              408  LOAD_CONST               12
              410  BINARY_SUBTRACT  
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  BINARY_ADD       
              416  STORE_FAST               'speak'
            418_0  COME_FROM           400  '400'
            418_1  COME_FROM           376  '376'
            418_2  COME_FROM           346  '346'

 L. 286       418  LOAD_FAST                'minute'
              420  LOAD_CONST               0
              422  COMPARE_OP               !=
          424_426  POP_JUMP_IF_FALSE   532  'to 532'

 L. 288       428  LOAD_FAST                'minute'
              430  LOAD_CONST               15
              432  COMPARE_OP               ==
          434_436  POP_JUMP_IF_FALSE   448  'to 448'

 L. 289       438  LOAD_FAST                'speak'
              440  LOAD_STR                 ' y cuarto'
              442  INPLACE_ADD      
              444  STORE_FAST               'speak'
              446  JUMP_FORWARD        532  'to 532'
            448_0  COME_FROM           434  '434'

 L. 290       448  LOAD_FAST                'minute'
              450  LOAD_CONST               30
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   468  'to 468'

 L. 291       458  LOAD_FAST                'speak'
              460  LOAD_STR                 ' y media'
              462  INPLACE_ADD      
              464  STORE_FAST               'speak'
              466  JUMP_FORWARD        532  'to 532'
            468_0  COME_FROM           454  '454'

 L. 292       468  LOAD_FAST                'minute'
              470  LOAD_CONST               -15
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   488  'to 488'

 L. 293       478  LOAD_FAST                'speak'
              480  LOAD_STR                 ' menos cuarto'
              482  INPLACE_ADD      
              484  STORE_FAST               'speak'
              486  JUMP_FORWARD        532  'to 532'
            488_0  COME_FROM           474  '474'

 L. 295       488  LOAD_FAST                'minute'
              490  LOAD_CONST               0
              492  COMPARE_OP               >
          494_496  POP_JUMP_IF_FALSE   516  'to 516'

 L. 296       498  LOAD_FAST                'speak'
              500  LOAD_STR                 ' y '
              502  LOAD_GLOBAL              pronounce_number_es
              504  LOAD_FAST                'minute'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  BINARY_ADD       
              510  INPLACE_ADD      
              512  STORE_FAST               'speak'
              514  JUMP_FORWARD        532  'to 532'
            516_0  COME_FROM           494  '494'

 L. 298       516  LOAD_FAST                'speak'
              518  LOAD_STR                 ' '
              520  LOAD_GLOBAL              pronounce_number_es
              522  LOAD_FAST                'minute'
              524  CALL_FUNCTION_1       1  '1 positional argument'
              526  BINARY_ADD       
              528  INPLACE_ADD      
              530  STORE_FAST               'speak'
            532_0  COME_FROM           514  '514'
            532_1  COME_FROM           486  '486'
            532_2  COME_FROM           466  '466'
            532_3  COME_FROM           446  '446'
            532_4  COME_FROM           424  '424'

 L. 301       532  LOAD_FAST                'minute'
              534  LOAD_CONST               0
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   556  'to 556'
              542  LOAD_FAST                'use_ampm'
          544_546  POP_JUMP_IF_TRUE    556  'to 556'

 L. 303       548  LOAD_FAST                'speak'
              550  LOAD_STR                 ' en punto'
              552  INPLACE_ADD      
              554  STORE_FAST               'speak'
            556_0  COME_FROM           544  '544'
            556_1  COME_FROM           538  '538'

 L. 305       556  LOAD_FAST                'use_ampm'
          558_560  POP_JUMP_IF_FALSE   660  'to 660'

 L. 312       562  LOAD_FAST                'hour'
              564  LOAD_CONST               0
              566  COMPARE_OP               >=
          568_570  POP_JUMP_IF_FALSE   592  'to 592'
              572  LOAD_FAST                'hour'
              574  LOAD_CONST               6
              576  COMPARE_OP               <
          578_580  POP_JUMP_IF_FALSE   592  'to 592'

 L. 313       582  LOAD_FAST                'speak'
              584  LOAD_STR                 ' de la madrugada'
              586  INPLACE_ADD      
              588  STORE_FAST               'speak'
              590  JUMP_FORWARD        660  'to 660'
            592_0  COME_FROM           578  '578'
            592_1  COME_FROM           568  '568'

 L. 314       592  LOAD_FAST                'hour'
              594  LOAD_CONST               6
              596  COMPARE_OP               >=
          598_600  POP_JUMP_IF_FALSE   622  'to 622'
              602  LOAD_FAST                'hour'
              604  LOAD_CONST               13
              606  COMPARE_OP               <
          608_610  POP_JUMP_IF_FALSE   622  'to 622'

 L. 315       612  LOAD_FAST                'speak'
              614  LOAD_STR                 ' de la mañana'
              616  INPLACE_ADD      
              618  STORE_FAST               'speak'
              620  JUMP_FORWARD        660  'to 660'
            622_0  COME_FROM           608  '608'
            622_1  COME_FROM           598  '598'

 L. 316       622  LOAD_FAST                'hour'
              624  LOAD_CONST               13
              626  COMPARE_OP               >=
          628_630  POP_JUMP_IF_FALSE   652  'to 652'
              632  LOAD_FAST                'hour'
              634  LOAD_CONST               21
              636  COMPARE_OP               <
            638_0  COME_FROM           148  '148'
          638_640  POP_JUMP_IF_FALSE   652  'to 652'

 L. 317       642  LOAD_FAST                'speak'
              644  LOAD_STR                 ' de la tarde'
              646  INPLACE_ADD      
              648  STORE_FAST               'speak'
              650  JUMP_FORWARD        660  'to 660'
            652_0  COME_FROM           638  '638'
            652_1  COME_FROM           628  '628'

 L. 319       652  LOAD_FAST                'speak'
              654  LOAD_STR                 ' de la noche'
              656  INPLACE_ADD      
              658  STORE_FAST               'speak'
            660_0  COME_FROM           650  '650'
            660_1  COME_FROM           620  '620'
            660_2  COME_FROM           590  '590'
            660_3  COME_FROM           558  '558'
            660_4  COME_FROM           168  '168'

 L. 320       660  LOAD_FAST                'speak'
              662  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 638_640