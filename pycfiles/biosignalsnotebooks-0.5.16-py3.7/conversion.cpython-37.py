# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\conversion.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 13761 bytes
"""
Module responsible for the definition of functions that convert Raw units (available in the
acquisition files returned by OpenSignals) and sample units to physical units like mV, A, ºC,
s,..., accordingly to the sensor under analysis.

Available Functions
-------------------
[Public]

raw_to_phy
    Function that converts each sample value in raw units to a physical unit taking into account
    the respective transfer function for the sensor and device specified as an input.
generate_time
    Considering the acquisition sampling rate and the number of samples that compose
    the signal, this function will return a time axis in seconds.

Observations/Comments
---------------------
None

/"""
import numpy
from .aux_functions import _is_a_url, _generate_download_google_link
from .load import load

def raw_to_phy--- This code section failed: ---

 L.  92         0  LOAD_GLOBAL              numpy
                2  LOAD_METHOD              array
                4  LOAD_FAST                'raw_signal'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'raw_signal'

 L.  95        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'resolution'
               14  LOAD_GLOBAL              int
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  POP_JUMP_IF_TRUE     40  'to 40'
               20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'resolution'
               24  LOAD_GLOBAL              numpy
               26  LOAD_ATTR                int32
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  POP_JUMP_IF_TRUE     40  'to 40'

 L.  96        32  LOAD_GLOBAL              RuntimeError
               34  LOAD_STR                 'The specified resolution needs to be an integer.'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'
             40_1  COME_FROM            18  '18'

 L.  98        40  LOAD_CONST               None
               42  STORE_FAST               'out'

 L.  99        44  LOAD_FAST                'sensor'
               46  LOAD_STR                 'TEMP'
               48  COMPARE_OP               ==
            50_52  POP_JUMP_IF_FALSE   344  'to 344'

 L. 100        54  LOAD_CONST               3.0
               56  STORE_FAST               'vcc'

 L. 101        58  LOAD_STR                 'bioplux'
               60  LOAD_STR                 'bioplux_exp'
               62  LOAD_STR                 'biosignalsplux'
               64  LOAD_STR                 'rachimeter'
               66  LOAD_STR                 'channeller'

 L. 102        68  LOAD_STR                 'swifter'
               70  LOAD_STR                 'ddme_openbanplux'
               72  BUILD_LIST_7          7 
               74  STORE_FAST               'available_dev_1'

 L. 103        76  LOAD_STR                 'bitalino'
               78  LOAD_STR                 'bitalino_rev'
               80  LOAD_STR                 'bitalino_riot'
               82  BUILD_LIST_3          3 
               84  STORE_FAST               'available_dev_2'

 L. 104        86  LOAD_FAST                'option'
               88  LOAD_STR                 'Ohm'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   134  'to 134'

 L. 105        94  LOAD_FAST                'device'
               96  LOAD_FAST                'available_dev_1'
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   124  'to 124'

 L. 106       102  LOAD_CONST               10000.0
              104  LOAD_FAST                'raw_signal'
              106  BINARY_MULTIPLY  
              108  LOAD_CONST               2
              110  LOAD_FAST                'resolution'
              112  BINARY_POWER     
              114  LOAD_FAST                'raw_signal'
              116  BINARY_SUBTRACT  
              118  BINARY_TRUE_DIVIDE
              120  STORE_FAST               'out'
              122  JUMP_FORWARD        132  'to 132'
            124_0  COME_FROM           100  '100'

 L. 108       124  LOAD_GLOBAL              RuntimeError
              126  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           122  '122'
              132  JUMP_FORWARD       1608  'to 1608'
            134_0  COME_FROM            92  '92'

 L. 110       134  LOAD_FAST                'option'
              136  LOAD_STR                 'K'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   232  'to 232'

 L. 111       142  LOAD_CONST               0.00112764514
              144  STORE_FAST               'a_0'

 L. 112       146  LOAD_CONST               0.000234282709
              148  STORE_FAST               'a_1'

 L. 113       150  LOAD_CONST               8.77303013e-08
              152  STORE_FAST               'a_2'

 L. 114       154  LOAD_CONST               1

 L. 115       156  LOAD_FAST                'a_0'
              158  LOAD_FAST                'a_1'
              160  LOAD_GLOBAL              numpy
              162  LOAD_METHOD              log
              164  LOAD_GLOBAL              raw_to_phy
              166  LOAD_FAST                'sensor'
              168  LOAD_FAST                'device'
              170  LOAD_GLOBAL              list
              172  LOAD_FAST                'raw_signal'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  LOAD_FAST                'resolution'
              178  LOAD_STR                 'Ohm'
              180  LOAD_CONST               ('option',)
              182  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  BINARY_MULTIPLY  
              188  BINARY_ADD       
              190  LOAD_FAST                'a_2'

 L. 116       192  LOAD_GLOBAL              numpy
              194  LOAD_METHOD              log
              196  LOAD_GLOBAL              raw_to_phy
              198  LOAD_FAST                'sensor'
              200  LOAD_FAST                'device'
              202  LOAD_GLOBAL              list
              204  LOAD_FAST                'raw_signal'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  LOAD_FAST                'resolution'

 L. 117       210  LOAD_STR                 'Ohm'
              212  LOAD_CONST               ('option',)
              214  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  LOAD_CONST               3
              220  BINARY_POWER     
              222  BINARY_MULTIPLY  
              224  BINARY_ADD       
              226  BINARY_TRUE_DIVIDE
              228  STORE_FAST               'out'
              230  JUMP_FORWARD       1608  'to 1608'
            232_0  COME_FROM           140  '140'

 L. 118       232  LOAD_FAST                'option'
              234  LOAD_STR                 'C'
              236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   332  'to 332'

 L. 119       242  LOAD_FAST                'device'
              244  LOAD_FAST                'available_dev_1'
              246  COMPARE_OP               in
          248_250  POP_JUMP_IF_FALSE   286  'to 286'

 L. 120       252  LOAD_GLOBAL              numpy
              254  LOAD_METHOD              array
              256  LOAD_GLOBAL              raw_to_phy
              258  LOAD_FAST                'sensor'
              260  LOAD_FAST                'device'
              262  LOAD_GLOBAL              list
              264  LOAD_FAST                'raw_signal'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  LOAD_FAST                'resolution'

 L. 121       270  LOAD_STR                 'K'
              272  LOAD_CONST               ('option',)
              274  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              276  CALL_METHOD_1         1  '1 positional argument'
              278  LOAD_CONST               273.15
              280  BINARY_SUBTRACT  
              282  STORE_FAST               'out'
              284  JUMP_FORWARD        330  'to 330'
            286_0  COME_FROM           248  '248'

 L. 122       286  LOAD_FAST                'device'
              288  LOAD_FAST                'available_dev_2'
              290  COMPARE_OP               in
          292_294  POP_JUMP_IF_FALSE   322  'to 322'

 L. 123       296  LOAD_FAST                'raw_signal'
              298  LOAD_CONST               2
              300  LOAD_FAST                'resolution'
              302  BINARY_POWER     
              304  BINARY_TRUE_DIVIDE
              306  LOAD_FAST                'vcc'
              308  BINARY_MULTIPLY  
              310  LOAD_CONST               0.5
              312  BINARY_SUBTRACT  
              314  LOAD_CONST               100
              316  BINARY_MULTIPLY  
              318  STORE_FAST               'out'
              320  JUMP_FORWARD        330  'to 330'
            322_0  COME_FROM           292  '292'

 L. 125       322  LOAD_GLOBAL              RuntimeError
              324  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  RAISE_VARARGS_1       1  'exception instance'
            330_0  COME_FROM           320  '320'
            330_1  COME_FROM           284  '284'
              330  JUMP_FORWARD       1608  'to 1608'
            332_0  COME_FROM           238  '238'

 L. 128       332  LOAD_GLOBAL              RuntimeError
              334  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
              336  CALL_FUNCTION_1       1  '1 positional argument'
              338  RAISE_VARARGS_1       1  'exception instance'
          340_342  JUMP_FORWARD       1608  'to 1608'
            344_0  COME_FROM            50  '50'

 L. 130       344  LOAD_FAST                'sensor'
              346  LOAD_STR                 'EMG'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   562  'to 562'

 L. 131       354  LOAD_STR                 'bioplux'
              356  LOAD_STR                 'bioplux_exp'
              358  LOAD_STR                 'biosignalsplux'
              360  LOAD_STR                 'rachimeter'
              362  LOAD_STR                 'channeller'

 L. 132       364  LOAD_STR                 'swifter'
              366  LOAD_STR                 'ddme_openbanplux'
              368  BUILD_LIST_7          7 
              370  STORE_FAST               'available_dev_1'

 L. 133       372  LOAD_STR                 'bitalino'
              374  BUILD_LIST_1          1 
              376  STORE_FAST               'available_dev_2'

 L. 134       378  LOAD_STR                 'bitalino_rev'
              380  LOAD_STR                 'bitalino_riot'
              382  BUILD_LIST_2          2 
              384  STORE_FAST               'available_dev_3'

 L. 135       386  LOAD_FAST                'option'
              388  LOAD_STR                 'mV'
              390  COMPARE_OP               ==
          392_394  POP_JUMP_IF_FALSE   506  'to 506'

 L. 136       396  LOAD_FAST                'device'
              398  LOAD_FAST                'available_dev_1'
              400  COMPARE_OP               in
          402_404  POP_JUMP_IF_FALSE   420  'to 420'

 L. 137       406  LOAD_CONST               3.0
              408  STORE_FAST               'vcc'

 L. 138       410  LOAD_CONST               0.5
              412  STORE_FAST               'offset'

 L. 139       414  LOAD_CONST               1
              416  STORE_FAST               'gain'
              418  JUMP_FORWARD        476  'to 476'
            420_0  COME_FROM           402  '402'

 L. 140       420  LOAD_FAST                'device'
              422  LOAD_FAST                'available_dev_2'
              424  COMPARE_OP               in
          426_428  POP_JUMP_IF_FALSE   444  'to 444'

 L. 141       430  LOAD_CONST               3.3
              432  STORE_FAST               'vcc'

 L. 142       434  LOAD_CONST               0.5
              436  STORE_FAST               'offset'

 L. 143       438  LOAD_CONST               1.008
              440  STORE_FAST               'gain'
              442  JUMP_FORWARD        476  'to 476'
            444_0  COME_FROM           426  '426'

 L. 144       444  LOAD_FAST                'device'
              446  LOAD_FAST                'available_dev_3'
              448  COMPARE_OP               in
          450_452  POP_JUMP_IF_FALSE   468  'to 468'

 L. 145       454  LOAD_CONST               3.3
              456  STORE_FAST               'vcc'

 L. 146       458  LOAD_CONST               0.5
              460  STORE_FAST               'offset'

 L. 147       462  LOAD_CONST               1.009
              464  STORE_FAST               'gain'
              466  JUMP_FORWARD        476  'to 476'
            468_0  COME_FROM           450  '450'

 L. 149       468  LOAD_GLOBAL              RuntimeError
              470  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  RAISE_VARARGS_1       1  'exception instance'
            476_0  COME_FROM           466  '466'
            476_1  COME_FROM           442  '442'
            476_2  COME_FROM           418  '418'

 L. 151       476  LOAD_FAST                'raw_signal'
              478  LOAD_FAST                'vcc'
              480  BINARY_MULTIPLY  
              482  LOAD_CONST               2
              484  LOAD_FAST                'resolution'
              486  BINARY_POWER     
              488  BINARY_TRUE_DIVIDE
              490  LOAD_FAST                'vcc'
              492  LOAD_FAST                'offset'
              494  BINARY_MULTIPLY  
              496  BINARY_SUBTRACT  
              498  LOAD_FAST                'gain'
              500  BINARY_TRUE_DIVIDE
              502  STORE_FAST               'out'
              504  JUMP_FORWARD       1608  'to 1608'
            506_0  COME_FROM           392  '392'

 L. 153       506  LOAD_FAST                'option'
              508  LOAD_STR                 'V'
              510  COMPARE_OP               ==
          512_514  POP_JUMP_IF_FALSE   550  'to 550'

 L. 154       516  LOAD_GLOBAL              numpy
              518  LOAD_METHOD              array
              520  LOAD_GLOBAL              raw_to_phy
              522  LOAD_FAST                'sensor'
              524  LOAD_FAST                'device'
              526  LOAD_GLOBAL              list
              528  LOAD_FAST                'raw_signal'
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  LOAD_FAST                'resolution'

 L. 155       534  LOAD_STR                 'mV'
              536  LOAD_CONST               ('option',)
              538  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  LOAD_CONST               1000
              544  BINARY_TRUE_DIVIDE
              546  STORE_FAST               'out'
              548  JUMP_FORWARD       1608  'to 1608'
            550_0  COME_FROM           512  '512'

 L. 158       550  LOAD_GLOBAL              RuntimeError
              552  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  RAISE_VARARGS_1       1  'exception instance'
          558_560  JUMP_FORWARD       1608  'to 1608'
            562_0  COME_FROM           350  '350'

 L. 160       562  LOAD_FAST                'sensor'
              564  LOAD_STR                 'ECG'
              566  COMPARE_OP               ==
          568_570  POP_JUMP_IF_FALSE   752  'to 752'

 L. 161       572  LOAD_STR                 'bioplux'
              574  LOAD_STR                 'bioplux_exp'
              576  LOAD_STR                 'biosignalsplux'
              578  LOAD_STR                 'rachimeter'
              580  LOAD_STR                 'channeller'

 L. 162       582  LOAD_STR                 'swifter'
              584  LOAD_STR                 'ddme_openbanplux'
              586  BUILD_LIST_7          7 
              588  STORE_FAST               'available_dev_1'

 L. 163       590  LOAD_STR                 'bitalino'
              592  LOAD_STR                 'bitalino_rev'
              594  LOAD_STR                 'bitalino_riot'
              596  BUILD_LIST_3          3 
              598  STORE_FAST               'available_dev_2'

 L. 164       600  LOAD_FAST                'option'
              602  LOAD_STR                 'mV'
              604  COMPARE_OP               ==
          606_608  POP_JUMP_IF_FALSE   696  'to 696'

 L. 165       610  LOAD_FAST                'device'
              612  LOAD_FAST                'available_dev_1'
              614  COMPARE_OP               in
          616_618  POP_JUMP_IF_FALSE   634  'to 634'

 L. 166       620  LOAD_CONST               3.0
              622  STORE_FAST               'vcc'

 L. 167       624  LOAD_CONST               0.5
              626  STORE_FAST               'offset'

 L. 168       628  LOAD_CONST               1.019
              630  STORE_FAST               'gain'
              632  JUMP_FORWARD        666  'to 666'
            634_0  COME_FROM           616  '616'

 L. 169       634  LOAD_FAST                'device'
              636  LOAD_FAST                'available_dev_2'
              638  COMPARE_OP               in
          640_642  POP_JUMP_IF_FALSE   658  'to 658'

 L. 170       644  LOAD_CONST               3.3
              646  STORE_FAST               'vcc'

 L. 171       648  LOAD_CONST               0.5
              650  STORE_FAST               'offset'

 L. 172       652  LOAD_CONST               1.1
              654  STORE_FAST               'gain'
              656  JUMP_FORWARD        666  'to 666'
            658_0  COME_FROM           640  '640'

 L. 174       658  LOAD_GLOBAL              RuntimeError
              660  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
              662  CALL_FUNCTION_1       1  '1 positional argument'
              664  RAISE_VARARGS_1       1  'exception instance'
            666_0  COME_FROM           656  '656'
            666_1  COME_FROM           632  '632'

 L. 176       666  LOAD_FAST                'raw_signal'
              668  LOAD_FAST                'vcc'
              670  BINARY_MULTIPLY  
              672  LOAD_CONST               2
              674  LOAD_FAST                'resolution'
              676  BINARY_POWER     
              678  BINARY_TRUE_DIVIDE
              680  LOAD_FAST                'vcc'
              682  LOAD_FAST                'offset'
              684  BINARY_MULTIPLY  
              686  BINARY_SUBTRACT  
              688  LOAD_FAST                'gain'
              690  BINARY_TRUE_DIVIDE
              692  STORE_FAST               'out'
              694  JUMP_FORWARD       1608  'to 1608'
            696_0  COME_FROM           606  '606'

 L. 178       696  LOAD_FAST                'option'
              698  LOAD_STR                 'V'
              700  COMPARE_OP               ==
          702_704  POP_JUMP_IF_FALSE   740  'to 740'

 L. 179       706  LOAD_GLOBAL              numpy
              708  LOAD_METHOD              array
              710  LOAD_GLOBAL              raw_to_phy
              712  LOAD_FAST                'sensor'
              714  LOAD_FAST                'device'
              716  LOAD_GLOBAL              list
              718  LOAD_FAST                'raw_signal'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  LOAD_FAST                'resolution'

 L. 180       724  LOAD_STR                 'mV'
              726  LOAD_CONST               ('option',)
              728  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              730  CALL_METHOD_1         1  '1 positional argument'
              732  LOAD_CONST               1000
              734  BINARY_TRUE_DIVIDE
              736  STORE_FAST               'out'
              738  JUMP_FORWARD       1608  'to 1608'
            740_0  COME_FROM           702  '702'

 L. 183       740  LOAD_GLOBAL              RuntimeError
              742  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  RAISE_VARARGS_1       1  'exception instance'
          748_750  JUMP_FORWARD       1608  'to 1608'
            752_0  COME_FROM           568  '568'

 L. 185       752  LOAD_FAST                'sensor'
              754  LOAD_STR                 'BVP'
              756  COMPARE_OP               ==
          758_760  POP_JUMP_IF_FALSE   908  'to 908'

 L. 186       762  LOAD_STR                 'bioplux'
              764  LOAD_STR                 'bioplux_exp'
              766  LOAD_STR                 'biosignalsplux'
              768  LOAD_STR                 'rachimeter'
              770  LOAD_STR                 'channeller'

 L. 187       772  LOAD_STR                 'swifter'
              774  LOAD_STR                 'ddme_openbanplux'
              776  BUILD_LIST_7          7 
              778  STORE_FAST               'available_dev_1'

 L. 188       780  LOAD_FAST                'option'
              782  LOAD_STR                 'uA'
              784  COMPARE_OP               ==
          786_788  POP_JUMP_IF_FALSE   852  'to 852'

 L. 189       790  LOAD_CONST               3.0
              792  STORE_FAST               'vcc'

 L. 190       794  LOAD_FAST                'device'
              796  LOAD_FAST                'available_dev_1'
              798  COMPARE_OP               in
          800_802  POP_JUMP_IF_FALSE   814  'to 814'

 L. 191       804  LOAD_CONST               0
              806  STORE_FAST               'offset'

 L. 192       808  LOAD_CONST               0.190060606
              810  STORE_FAST               'gain'
              812  JUMP_FORWARD        822  'to 822'
            814_0  COME_FROM           800  '800'

 L. 194       814  LOAD_GLOBAL              RuntimeError
              816  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
              818  CALL_FUNCTION_1       1  '1 positional argument'
              820  RAISE_VARARGS_1       1  'exception instance'
            822_0  COME_FROM           812  '812'

 L. 196       822  LOAD_FAST                'raw_signal'
              824  LOAD_FAST                'vcc'
              826  BINARY_MULTIPLY  
              828  LOAD_CONST               2
              830  LOAD_FAST                'resolution'
              832  BINARY_POWER     
              834  BINARY_TRUE_DIVIDE
              836  LOAD_FAST                'vcc'
              838  LOAD_FAST                'offset'
              840  BINARY_MULTIPLY  
              842  BINARY_SUBTRACT  
              844  LOAD_FAST                'gain'
              846  BINARY_TRUE_DIVIDE
              848  STORE_FAST               'out'
              850  JUMP_FORWARD       1608  'to 1608'
            852_0  COME_FROM           786  '786'

 L. 198       852  LOAD_FAST                'option'
              854  LOAD_STR                 'A'
              856  COMPARE_OP               ==
          858_860  POP_JUMP_IF_FALSE   896  'to 896'

 L. 199       862  LOAD_GLOBAL              numpy
              864  LOAD_METHOD              array
              866  LOAD_GLOBAL              raw_to_phy
              868  LOAD_FAST                'sensor'
              870  LOAD_FAST                'device'
              872  LOAD_GLOBAL              list
              874  LOAD_FAST                'raw_signal'
              876  CALL_FUNCTION_1       1  '1 positional argument'
              878  LOAD_FAST                'resolution'

 L. 200       880  LOAD_STR                 'uA'
              882  LOAD_CONST               ('option',)
              884  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              886  CALL_METHOD_1         1  '1 positional argument'
              888  LOAD_CONST               1e-06
              890  BINARY_MULTIPLY  
              892  STORE_FAST               'out'
              894  JUMP_FORWARD       1608  'to 1608'
            896_0  COME_FROM           858  '858'

 L. 203       896  LOAD_GLOBAL              RuntimeError
              898  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  RAISE_VARARGS_1       1  'exception instance'
          904_906  JUMP_FORWARD       1608  'to 1608'
            908_0  COME_FROM           758  '758'

 L. 205       908  LOAD_FAST                'sensor'
              910  LOAD_CONST               ('SpO2.ARM', 'SpO2.HEAD', 'SpO2.FING')
              912  COMPARE_OP               in
          914_916  POP_JUMP_IF_FALSE  1076  'to 1076'

 L. 206       918  LOAD_STR                 'channeller'
              920  LOAD_STR                 'biosignalsplux'
              922  LOAD_STR                 'swifter'
              924  BUILD_LIST_3          3 
              926  STORE_FAST               'available_dev_1'

 L. 208       928  LOAD_CONST               None
              930  STORE_FAST               'scale_factor'

 L. 209       932  LOAD_STR                 'ARM'
              934  LOAD_FAST                'sensor'
              936  COMPARE_OP               in
          938_940  POP_JUMP_IF_TRUE    952  'to 952'
              942  LOAD_STR                 'FING'
              944  LOAD_FAST                'sensor'
              946  COMPARE_OP               in
          948_950  POP_JUMP_IF_FALSE   958  'to 958'
            952_0  COME_FROM           938  '938'

 L. 210       952  LOAD_CONST               1.2
              954  STORE_FAST               'scale_factor'
              956  JUMP_FORWARD        972  'to 972'
            958_0  COME_FROM           948  '948'

 L. 211       958  LOAD_STR                 'HEAD'
              960  LOAD_FAST                'sensor'
              962  COMPARE_OP               in
          964_966  POP_JUMP_IF_FALSE   972  'to 972'

 L. 212       968  LOAD_CONST               0.15
              970  STORE_FAST               'scale_factor'
            972_0  COME_FROM           964  '964'
            972_1  COME_FROM           956  '956'

 L. 214       972  LOAD_FAST                'option'
              974  LOAD_STR                 'uA'
              976  COMPARE_OP               ==
          978_980  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 215       982  LOAD_FAST                'device'
              984  LOAD_FAST                'available_dev_1'
              986  COMPARE_OP               in
          988_990  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 216       992  LOAD_FAST                'scale_factor'
              994  LOAD_FAST                'raw_signal'
              996  LOAD_CONST               2
              998  LOAD_FAST                'resolution'
             1000  BINARY_POWER     
             1002  BINARY_TRUE_DIVIDE
             1004  BINARY_MULTIPLY  
             1006  STORE_FAST               'out'
             1008  JUMP_FORWARD       1018  'to 1018'
           1010_0  COME_FROM           988  '988'

 L. 218      1010  LOAD_GLOBAL              RuntimeError
             1012  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
             1014  CALL_FUNCTION_1       1  '1 positional argument'
             1016  RAISE_VARARGS_1       1  'exception instance'
           1018_0  COME_FROM          1008  '1008'
             1018  JUMP_FORWARD       1608  'to 1608'
           1020_0  COME_FROM           978  '978'

 L. 221      1020  LOAD_FAST                'option'
             1022  LOAD_STR                 'A'
             1024  COMPARE_OP               ==
         1026_1028  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 222      1030  LOAD_GLOBAL              numpy
             1032  LOAD_METHOD              array
             1034  LOAD_GLOBAL              raw_to_phy
             1036  LOAD_FAST                'sensor'
             1038  LOAD_FAST                'device'
             1040  LOAD_GLOBAL              list
             1042  LOAD_FAST                'raw_signal'
             1044  CALL_FUNCTION_1       1  '1 positional argument'
             1046  LOAD_FAST                'resolution'

 L. 223      1048  LOAD_STR                 'uA'
             1050  LOAD_CONST               ('option',)
             1052  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1054  CALL_METHOD_1         1  '1 positional argument'
             1056  LOAD_CONST               1e-06
             1058  BINARY_MULTIPLY  
             1060  STORE_FAST               'out'
             1062  JUMP_FORWARD       1608  'to 1608'
           1064_0  COME_FROM          1026  '1026'

 L. 226      1064  LOAD_GLOBAL              RuntimeError
             1066  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  RAISE_VARARGS_1       1  'exception instance'
         1072_1074  JUMP_FORWARD       1608  'to 1608'
           1076_0  COME_FROM           914  '914'

 L. 228      1076  LOAD_FAST                'sensor'
             1078  LOAD_STR                 'ACC'
             1080  COMPARE_OP               ==
         1082_1084  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 229      1086  LOAD_STR                 'bioplux'
             1088  LOAD_STR                 'bioplux_exp'
             1090  LOAD_STR                 'biosignalsplux'
             1092  LOAD_STR                 'rachimeter'
             1094  LOAD_STR                 'channeller'

 L. 230      1096  LOAD_STR                 'swifter'
             1098  LOAD_STR                 'ddme_openbanplux'
             1100  BUILD_LIST_7          7 
             1102  STORE_FAST               'available_dev_1'

 L. 231      1104  LOAD_FAST                'option'
             1106  LOAD_STR                 'g'
             1108  COMPARE_OP               ==
         1110_1112  POP_JUMP_IF_FALSE  1180  'to 1180'

 L. 232      1114  LOAD_FAST                'device'
             1116  LOAD_FAST                'available_dev_1'
             1118  COMPARE_OP               in
         1120_1122  POP_JUMP_IF_FALSE  1134  'to 1134'

 L. 233      1124  LOAD_CONST               28000.0
             1126  STORE_FAST               'Cm'

 L. 234      1128  LOAD_CONST               38000.0
             1130  STORE_FAST               'CM'
             1132  JUMP_FORWARD       1142  'to 1142'
           1134_0  COME_FROM          1120  '1120'

 L. 236      1134  LOAD_GLOBAL              RuntimeError
             1136  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
             1138  CALL_FUNCTION_1       1  '1 positional argument'
             1140  RAISE_VARARGS_1       1  'exception instance'
           1142_0  COME_FROM          1132  '1132'

 L. 239      1142  LOAD_CONST               2.0
             1144  LOAD_CONST               2
             1146  LOAD_CONST               16.0
             1148  LOAD_FAST                'resolution'
             1150  BINARY_SUBTRACT  
             1152  BINARY_POWER     
             1154  LOAD_FAST                'raw_signal'
             1156  BINARY_MULTIPLY  
             1158  LOAD_FAST                'Cm'
             1160  BINARY_SUBTRACT  
             1162  LOAD_FAST                'CM'
             1164  LOAD_FAST                'Cm'
             1166  BINARY_SUBTRACT  
             1168  BINARY_TRUE_DIVIDE
             1170  BINARY_MULTIPLY  
             1172  LOAD_CONST               1.0
             1174  BINARY_SUBTRACT  
             1176  STORE_FAST               'out'
             1178  JUMP_FORWARD       1608  'to 1608'
           1180_0  COME_FROM          1110  '1110'

 L. 242      1180  LOAD_GLOBAL              RuntimeError
             1182  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
             1184  CALL_FUNCTION_1       1  '1 positional argument'
             1186  RAISE_VARARGS_1       1  'exception instance'
         1188_1190  JUMP_FORWARD       1608  'to 1608'
           1192_0  COME_FROM          1082  '1082'

 L. 244      1192  LOAD_FAST                'sensor'
             1194  LOAD_STR                 'EEG'
             1196  COMPARE_OP               ==
         1198_1200  POP_JUMP_IF_FALSE  1378  'to 1378'

 L. 245      1202  LOAD_STR                 'bioplux'
             1204  LOAD_STR                 'bioplux_exp'
             1206  LOAD_STR                 'biosignalsplux'
             1208  LOAD_STR                 'rachimeter'
             1210  LOAD_STR                 'channeller'
             1212  LOAD_STR                 'swifter'

 L. 246      1214  LOAD_STR                 'ddme_openbanplux'
             1216  BUILD_LIST_7          7 
             1218  STORE_FAST               'available_dev_1'

 L. 247      1220  LOAD_STR                 'bitalino_rev'
             1222  LOAD_STR                 'bitalino_riot'
             1224  BUILD_LIST_2          2 
             1226  STORE_FAST               'available_dev_2'

 L. 248      1228  LOAD_FAST                'option'
             1230  LOAD_STR                 'uV'
             1232  COMPARE_OP               ==
         1234_1236  POP_JUMP_IF_FALSE  1324  'to 1324'

 L. 249      1238  LOAD_FAST                'device'
             1240  LOAD_FAST                'available_dev_1'
             1242  COMPARE_OP               in
         1244_1246  POP_JUMP_IF_FALSE  1262  'to 1262'

 L. 250      1248  LOAD_CONST               3.0
             1250  STORE_FAST               'vcc'

 L. 251      1252  LOAD_CONST               0.5
             1254  STORE_FAST               'offset'

 L. 252      1256  LOAD_CONST               0.04199
             1258  STORE_FAST               'gain'
             1260  JUMP_FORWARD       1294  'to 1294'
           1262_0  COME_FROM          1244  '1244'

 L. 253      1262  LOAD_FAST                'device'
             1264  LOAD_FAST                'available_dev_2'
             1266  COMPARE_OP               in
         1268_1270  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 254      1272  LOAD_CONST               3.3
             1274  STORE_FAST               'vcc'

 L. 255      1276  LOAD_CONST               0.5
             1278  STORE_FAST               'offset'

 L. 256      1280  LOAD_CONST               0.04
             1282  STORE_FAST               'gain'
             1284  JUMP_FORWARD       1294  'to 1294'
           1286_0  COME_FROM          1268  '1268'

 L. 258      1286  LOAD_GLOBAL              RuntimeError
             1288  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
             1290  CALL_FUNCTION_1       1  '1 positional argument'
             1292  RAISE_VARARGS_1       1  'exception instance'
           1294_0  COME_FROM          1284  '1284'
           1294_1  COME_FROM          1260  '1260'

 L. 260      1294  LOAD_FAST                'raw_signal'
             1296  LOAD_FAST                'vcc'
             1298  BINARY_MULTIPLY  
             1300  LOAD_CONST               2
             1302  LOAD_FAST                'resolution'
             1304  BINARY_POWER     
             1306  BINARY_TRUE_DIVIDE
             1308  LOAD_FAST                'vcc'
             1310  LOAD_FAST                'offset'
             1312  BINARY_MULTIPLY  
             1314  BINARY_SUBTRACT  
             1316  LOAD_FAST                'gain'
             1318  BINARY_TRUE_DIVIDE
             1320  STORE_FAST               'out'
             1322  JUMP_FORWARD       1376  'to 1376'
           1324_0  COME_FROM          1234  '1234'

 L. 262      1324  LOAD_FAST                'option'
             1326  LOAD_STR                 'V'
             1328  COMPARE_OP               ==
         1330_1332  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 263      1334  LOAD_GLOBAL              numpy
             1336  LOAD_METHOD              array
             1338  LOAD_GLOBAL              raw_to_phy
             1340  LOAD_FAST                'sensor'
             1342  LOAD_FAST                'device'
             1344  LOAD_GLOBAL              list
             1346  LOAD_FAST                'raw_signal'
             1348  CALL_FUNCTION_1       1  '1 positional argument'
             1350  LOAD_FAST                'resolution'

 L. 264      1352  LOAD_STR                 'uV'
             1354  LOAD_CONST               ('option',)
             1356  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1358  CALL_METHOD_1         1  '1 positional argument'
             1360  LOAD_CONST               1000000.0
             1362  BINARY_MULTIPLY  
             1364  STORE_FAST               'out'
             1366  JUMP_FORWARD       1376  'to 1376'
           1368_0  COME_FROM          1330  '1330'

 L. 267      1368  LOAD_GLOBAL              RuntimeError
             1370  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
             1372  CALL_FUNCTION_1       1  '1 positional argument'
             1374  RAISE_VARARGS_1       1  'exception instance'
           1376_0  COME_FROM          1366  '1366'
           1376_1  COME_FROM          1322  '1322'
             1376  JUMP_FORWARD       1608  'to 1608'
           1378_0  COME_FROM          1198  '1198'

 L. 269      1378  LOAD_FAST                'sensor'
             1380  LOAD_STR                 'EDA'
             1382  COMPARE_OP               ==
         1384_1386  POP_JUMP_IF_FALSE  1600  'to 1600'

 L. 270      1388  LOAD_STR                 'bioplux'
             1390  LOAD_STR                 'bioplux_exp'
             1392  LOAD_STR                 'biosignalsplux'
             1394  LOAD_STR                 'rachimeter'
             1396  LOAD_STR                 'channeller'
           1398_0  COME_FROM           132  '132'
             1398  LOAD_STR                 'swifter'

 L. 271      1400  LOAD_STR                 'biosignalspluxsolo'
             1402  BUILD_LIST_7          7 
             1404  STORE_FAST               'available_dev_1'

 L. 272      1406  LOAD_STR                 'bitalino'
             1408  BUILD_LIST_1          1 
             1410  STORE_FAST               'available_dev_2'

 L. 273      1412  LOAD_STR                 'bitalino_rev'
             1414  LOAD_STR                 'bitalino_riot'
             1416  BUILD_LIST_2          2 
             1418  STORE_FAST               'available_dev_3'

 L. 274      1420  LOAD_FAST                'option'
             1422  LOAD_STR                 'uS'
             1424  COMPARE_OP               ==
         1426_1428  POP_JUMP_IF_FALSE  1546  'to 1546'

 L. 275      1430  LOAD_FAST                'device'
             1432  LOAD_FAST                'available_dev_1'
             1434  COMPARE_OP               in
         1436_1438  POP_JUMP_IF_FALSE  1454  'to 1454'

 L. 276      1440  LOAD_CONST               3.0
             1442  STORE_FAST               'vcc'

 L. 277      1444  LOAD_CONST               0
             1446  STORE_FAST               'offset'

 L. 278      1448  LOAD_CONST               0.12
             1450  STORE_FAST               'gain'
             1452  JUMP_FORWARD       1516  'to 1516'
           1454_0  COME_FROM          1436  '1436'

 L. 279      1454  LOAD_FAST                'device'
             1456  LOAD_FAST                'available_dev_2'
             1458  COMPARE_OP               in
         1460_1462  POP_JUMP_IF_FALSE  1484  'to 1484'

 L. 280      1464  LOAD_CONST               1.0
             1466  LOAD_CONST               1.0
             1468  LOAD_FAST                'raw_signal'
             1470  LOAD_CONST               2
             1472  LOAD_FAST                'resolution'
             1474  BINARY_POWER     
             1476  BINARY_TRUE_DIVIDE
             1478  BINARY_SUBTRACT  
             1480  BINARY_TRUE_DIVIDE
             1482  RETURN_VALUE     
           1484_0  COME_FROM          1460  '1460'

 L. 281      1484  LOAD_FAST                'device'
             1486  LOAD_FAST                'available_dev_3'
             1488  COMPARE_OP               in
         1490_1492  POP_JUMP_IF_FALSE  1508  'to 1508'

 L. 282      1494  LOAD_CONST               3.3
           1496_0  COME_FROM           230  '230'
             1496  STORE_FAST               'vcc'

 L. 283      1498  LOAD_CONST               0
             1500  STORE_FAST               'offset'

 L. 284      1502  LOAD_CONST               0.132
             1504  STORE_FAST               'gain'
             1506  JUMP_FORWARD       1516  'to 1516'
           1508_0  COME_FROM          1490  '1490'

 L. 286      1508  LOAD_GLOBAL              RuntimeError
             1510  LOAD_STR                 'The output specified unit does not have a defined transfer function for the used device.'
             1512  CALL_FUNCTION_1       1  '1 positional argument'
             1514  RAISE_VARARGS_1       1  'exception instance'
           1516_0  COME_FROM          1506  '1506'
           1516_1  COME_FROM          1452  '1452'

 L. 288      1516  LOAD_FAST                'raw_signal'
             1518  LOAD_FAST                'vcc'
             1520  BINARY_MULTIPLY  
             1522  LOAD_CONST               2
             1524  LOAD_FAST                'resolution'
             1526  BINARY_POWER     
             1528  BINARY_TRUE_DIVIDE
             1530  LOAD_FAST                'vcc'
             1532  LOAD_FAST                'offset'
             1534  BINARY_MULTIPLY  
             1536  BINARY_SUBTRACT  
             1538  LOAD_FAST                'gain'
             1540  BINARY_TRUE_DIVIDE
             1542  STORE_FAST               'out'
             1544  JUMP_FORWARD       1598  'to 1598'
           1546_0  COME_FROM          1426  '1426'

 L. 290      1546  LOAD_FAST                'option'
             1548  LOAD_STR                 'S'
             1550  COMPARE_OP               ==
           1552_0  COME_FROM          1018  '1018'
           1552_1  COME_FROM           850  '850'
           1552_2  COME_FROM           694  '694'
           1552_3  COME_FROM           504  '504'
         1552_1554  POP_JUMP_IF_FALSE  1590  'to 1590'

 L. 291      1556  LOAD_GLOBAL              numpy
             1558  LOAD_METHOD              array
             1560  LOAD_GLOBAL              raw_to_phy
             1562  LOAD_FAST                'sensor'
             1564  LOAD_FAST                'device'
             1566  LOAD_GLOBAL              list
             1568  LOAD_FAST                'raw_signal'
             1570  CALL_FUNCTION_1       1  '1 positional argument'
             1572  LOAD_FAST                'resolution'

 L. 292      1574  LOAD_STR                 'uS'
             1576  LOAD_CONST               ('option',)
             1578  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1580  CALL_METHOD_1         1  '1 positional argument'
             1582  LOAD_CONST               1000000.0
             1584  BINARY_MULTIPLY  
             1586  STORE_FAST               'out'
             1588  JUMP_FORWARD       1598  'to 1598'
           1590_0  COME_FROM          1552  '1552'

 L. 295      1590  LOAD_GLOBAL              RuntimeError
             1592  LOAD_STR                 'The selected output unit is invalid for the sensor under analysis.'
             1594  CALL_FUNCTION_1       1  '1 positional argument'
           1596_0  COME_FROM          1178  '1178'
           1596_1  COME_FROM          1062  '1062'
           1596_2  COME_FROM           894  '894'
           1596_3  COME_FROM           738  '738'
           1596_4  COME_FROM           548  '548'
           1596_5  COME_FROM           330  '330'
             1596  RAISE_VARARGS_1       1  'exception instance'
           1598_0  COME_FROM          1588  '1588'
           1598_1  COME_FROM          1544  '1544'
             1598  JUMP_FORWARD       1608  'to 1608'
           1600_0  COME_FROM          1384  '1384'

 L. 298      1600  LOAD_GLOBAL              RuntimeError
             1602  LOAD_STR                 'The specified sensor is not valid or for now is not available for unit conversion.'
             1604  CALL_FUNCTION_1       1  '1 positional argument'
             1606  RAISE_VARARGS_1       1  'exception instance'
           1608_0  COME_FROM          1598  '1598'
           1608_1  COME_FROM          1376  '1376'
           1608_2  COME_FROM          1188  '1188'
           1608_3  COME_FROM          1072  '1072'
           1608_4  COME_FROM           904  '904'
           1608_5  COME_FROM           748  '748'
           1608_6  COME_FROM           558  '558'
           1608_7  COME_FROM           340  '340'

 L. 301      1608  LOAD_FAST                'out'
             1610  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1398_0


def generate_time(signal, sample_rate=1000):
    """
    -----
    Brief
    -----
    Function intended to generate a time axis of the input signal.

    -----------
    Description
    -----------
    The time axis generated by the acquisition process originates a set of consecutive values that represents the
    advancement of time, but does not have specific units.

    Once the acquisitions are made with specific sampling frequencies, it is possible to calculate the time instant
    of each sample by multiplying that value by the sampling frequency.

    The current function maps the values in the file produced by Opensignals to their real temporal values.

    ----------
    Parameters
    ----------
    signal : list
        List with the signal samples.

    sample_rate : int
        Sampling frequency of acquisition.

    Returns
    -------
    out : list
        Time axis with each list entry in seconds.
    """
    if _is_a_url(signal):
        if 'drive.google' in signal:
            signal = _generate_download_google_link(signal)
        data = load(signal, remote=True)
        key_level_1 = list(data.keys())[0]
        if '00:' in key_level_1:
            mac = key_level_1
            chn = list(data[mac].keys())[0]
            signal = data[mac][chn]
        else:
            chn = key_level_1
            signal = data[chn]
    nbr_of_samples = len(signal)
    end_of_time = nbr_of_samples / sample_rate
    time_axis = numpy.linspace(0, end_of_time, nbr_of_samples)
    return list(time_axis)