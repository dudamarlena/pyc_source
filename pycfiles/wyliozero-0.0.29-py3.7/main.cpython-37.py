# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/wyliozero/main.py
# Compiled at: 2019-11-24 09:28:29
# Size of source mod 2**32: 8498 bytes
from . import winclude as w
from gpiozero import *
from .wlcd import lcd as LabLCD
print('Setup pins')
Device.pin_factory = w.wfactory.WFactory()

def pause():
    print('Press Enter to end the program')
    raw_input()
    w._exit(0)


for eachPin in w.pinsAll:
    globals()[eachPin] = eachPin

class DHTsensor:

    def __init__(self, pin):
        self.pin = pin

    def humidityRead(self):
        return humidityRead(self.pin)

    def temperatureRead(self):
        return temperatureRead(self.pin)


def humidityRead--- This code section failed: ---

 L.  30         0  LOAD_GLOBAL              w
                2  LOAD_METHOD              isR
                4  LOAD_FAST                'pin'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_FALSE    36  'to 36'

 L.  31        10  LOAD_GLOBAL              w
               12  LOAD_METHOD              DHT_read_retry
               14  LOAD_CONST               11
               16  LOAD_GLOBAL              w
               18  LOAD_METHOD              p
               20  LOAD_FAST                'pin'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  CALL_METHOD_2         2  '2 positional arguments'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'x'
               30  STORE_FAST               'y'

 L.  32        32  LOAD_FAST                'x'
               34  RETURN_VALUE     
             36_0  COME_FROM             8  '8'

 L.  33        36  LOAD_GLOBAL              w
               38  LOAD_METHOD              isD
               40  LOAD_FAST                'pin'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_JUMP_IF_TRUE     86  'to 86'
               46  LOAD_GLOBAL              w
               48  LOAD_METHOD              isA
               50  LOAD_FAST                'pin'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_JUMP_IF_TRUE     86  'to 86'
               56  LOAD_GLOBAL              w
               58  LOAD_METHOD              isAdig
               60  LOAD_FAST                'pin'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_JUMP_IF_TRUE     86  'to 86'
               66  LOAD_GLOBAL              w
               68  LOAD_METHOD              isButton
               70  LOAD_FAST                'pin'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_JUMP_IF_TRUE     86  'to 86'
               76  LOAD_GLOBAL              w
               78  LOAD_METHOD              isLED
               80  LOAD_FAST                'pin'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_JUMP_IF_FALSE   106  'to 106'
             86_0  COME_FROM            74  '74'
             86_1  COME_FROM            64  '64'
             86_2  COME_FROM            54  '54'
             86_3  COME_FROM            44  '44'

 L.  34        86  LOAD_GLOBAL              w
               88  LOAD_ATTR                log
               90  LOAD_METHOD              error
               92  LOAD_STR                 'Pin {0} cannot be used to read humidity from it'
               94  LOAD_METHOD              format
               96  LOAD_FAST                'pin'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  POP_TOP          
              104  JUMP_FORWARD        120  'to 120'
            106_0  COME_FROM            84  '84'

 L.  36       106  LOAD_GLOBAL              w
              108  LOAD_ATTR                log
              110  LOAD_METHOD              error
              112  LOAD_FAST                'pin'
              114  LOAD_STR                 'arg'
              116  CALL_METHOD_2         2  '2 positional arguments'
              118  POP_TOP          
            120_0  COME_FROM           104  '104'

Parse error at or near `JUMP_FORWARD' instruction at offset 104


def temperatureRead--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              w
                2  LOAD_METHOD              isR
                4  LOAD_FAST                'pin'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_FALSE    36  'to 36'

 L.  41        10  LOAD_GLOBAL              w
               12  LOAD_METHOD              DHT_read_retry
               14  LOAD_CONST               11
               16  LOAD_GLOBAL              w
               18  LOAD_METHOD              p
               20  LOAD_FAST                'pin'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  CALL_METHOD_2         2  '2 positional arguments'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'x'
               30  STORE_FAST               'y'

 L.  42        32  LOAD_FAST                'y'
               34  RETURN_VALUE     
             36_0  COME_FROM             8  '8'

 L.  43        36  LOAD_GLOBAL              w
               38  LOAD_METHOD              isD
               40  LOAD_FAST                'pin'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_JUMP_IF_TRUE     86  'to 86'
               46  LOAD_GLOBAL              w
               48  LOAD_METHOD              isA
               50  LOAD_FAST                'pin'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_JUMP_IF_TRUE     86  'to 86'
               56  LOAD_GLOBAL              w
               58  LOAD_METHOD              isAdig
               60  LOAD_FAST                'pin'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_JUMP_IF_TRUE     86  'to 86'
               66  LOAD_GLOBAL              w
               68  LOAD_METHOD              isButton
               70  LOAD_FAST                'pin'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_JUMP_IF_TRUE     86  'to 86'
               76  LOAD_GLOBAL              w
               78  LOAD_METHOD              isLED
               80  LOAD_FAST                'pin'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  POP_JUMP_IF_FALSE   106  'to 106'
             86_0  COME_FROM            74  '74'
             86_1  COME_FROM            64  '64'
             86_2  COME_FROM            54  '54'
             86_3  COME_FROM            44  '44'

 L.  44        86  LOAD_GLOBAL              w
               88  LOAD_ATTR                log
               90  LOAD_METHOD              error
               92  LOAD_STR                 'Pin {0} cannot be used to read temperature from it'
               94  LOAD_METHOD              format
               96  LOAD_FAST                'pin'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  POP_TOP          
              104  JUMP_FORWARD        120  'to 120'
            106_0  COME_FROM            84  '84'

 L.  46       106  LOAD_GLOBAL              w
              108  LOAD_ATTR                log
              110  LOAD_METHOD              error
              112  LOAD_FAST                'pin'
              114  LOAD_STR                 'arg'
              116  CALL_METHOD_2         2  '2 positional arguments'
              118  POP_TOP          
            120_0  COME_FROM           104  '104'

Parse error at or near `JUMP_FORWARD' instruction at offset 104


INPUT = 'i'
OUTPUT = 'o'
HIGH = 1
LOW = 0

def pinMode--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              w
                2  LOAD_METHOD              isR
                4  LOAD_FAST                'pin'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  56     10_12  JUMP_FORWARD        778  'to 778'
             14_0  COME_FROM             8  '8'

 L.  58        14  LOAD_GLOBAL              w
               16  LOAD_METHOD              isDPWM
               18  LOAD_FAST                'pin'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_JUMP_IF_FALSE   150  'to 150'

 L.  59        24  LOAD_GLOBAL              w
               26  LOAD_METHOD              isOutput
               28  LOAD_FAST                'value'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.  60        34  LOAD_GLOBAL              w
               36  LOAD_ATTR                ard
               38  LOAD_METHOD              set_pin_mode
               40  LOAD_GLOBAL              w
               42  LOAD_METHOD              p
               44  LOAD_FAST                'pin'
               46  CALL_METHOD_1         1  '1 positional argument'
               48  LOAD_GLOBAL              w
               50  LOAD_ATTR                Constants
               52  LOAD_ATTR                PWM
               54  CALL_METHOD_2         2  '2 positional arguments'
               56  POP_TOP          
               58  JUMP_FORWARD        778  'to 778'
             60_0  COME_FROM            32  '32'

 L.  61        60  LOAD_GLOBAL              w
               62  LOAD_METHOD              isInput
               64  LOAD_FAST                'value'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  POP_JUMP_IF_FALSE    96  'to 96'

 L.  62        70  LOAD_GLOBAL              w
               72  LOAD_ATTR                ard
               74  LOAD_METHOD              set_pin_mode
               76  LOAD_GLOBAL              w
               78  LOAD_METHOD              p
               80  LOAD_FAST                'pin'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  LOAD_GLOBAL              w
               86  LOAD_ATTR                Constants
               88  LOAD_ATTR                INPUT
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  POP_TOP          
               94  JUMP_FORWARD        778  'to 778'
             96_0  COME_FROM            68  '68'

 L.  63        96  LOAD_GLOBAL              w
               98  LOAD_METHOD              isPullupInput
              100  LOAD_FAST                'value'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  POP_JUMP_IF_FALSE   132  'to 132'

 L.  64       106  LOAD_GLOBAL              w
              108  LOAD_ATTR                ard
              110  LOAD_METHOD              set_pin_mode
              112  LOAD_GLOBAL              w
              114  LOAD_METHOD              p
              116  LOAD_FAST                'pin'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  LOAD_GLOBAL              w
              122  LOAD_ATTR                Constants
              124  LOAD_ATTR                PULLUP
              126  CALL_METHOD_2         2  '2 positional arguments'
              128  POP_TOP          
              130  JUMP_FORWARD        778  'to 778'
            132_0  COME_FROM           104  '104'

 L.  66       132  LOAD_GLOBAL              w
              134  LOAD_ATTR                log
              136  LOAD_METHOD              error
              138  LOAD_FAST                'value'
              140  LOAD_STR                 'arg'
              142  CALL_METHOD_2         2  '2 positional arguments'
              144  POP_TOP          
          146_148  JUMP_FORWARD        778  'to 778'
            150_0  COME_FROM            22  '22'

 L.  68       150  LOAD_GLOBAL              w
              152  LOAD_METHOD              isD
              154  LOAD_FAST                'pin'
              156  CALL_METHOD_1         1  '1 positional argument'
          158_160  POP_JUMP_IF_FALSE   290  'to 290'

 L.  69       162  LOAD_GLOBAL              w
              164  LOAD_METHOD              isOutput
              166  LOAD_FAST                'value'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  POP_JUMP_IF_FALSE   198  'to 198'

 L.  70       172  LOAD_GLOBAL              w
              174  LOAD_ATTR                ard
              176  LOAD_METHOD              set_pin_mode
              178  LOAD_GLOBAL              w
              180  LOAD_METHOD              p
              182  LOAD_FAST                'pin'
              184  CALL_METHOD_1         1  '1 positional argument'
              186  LOAD_GLOBAL              w
              188  LOAD_ATTR                Constants
              190  LOAD_ATTR                OUTPUT
              192  CALL_METHOD_2         2  '2 positional arguments'
              194  POP_TOP          
              196  JUMP_FORWARD        778  'to 778'
            198_0  COME_FROM           170  '170'

 L.  71       198  LOAD_GLOBAL              w
              200  LOAD_METHOD              isInput
              202  LOAD_FAST                'value'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_JUMP_IF_FALSE   234  'to 234'

 L.  72       208  LOAD_GLOBAL              w
              210  LOAD_ATTR                ard
              212  LOAD_METHOD              set_pin_mode
              214  LOAD_GLOBAL              w
              216  LOAD_METHOD              p
              218  LOAD_FAST                'pin'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  LOAD_GLOBAL              w
              224  LOAD_ATTR                Constants
              226  LOAD_ATTR                INPUT
              228  CALL_METHOD_2         2  '2 positional arguments'
              230  POP_TOP          
              232  JUMP_FORWARD        778  'to 778'
            234_0  COME_FROM           206  '206'

 L.  73       234  LOAD_GLOBAL              w
              236  LOAD_METHOD              isPullupInput
              238  LOAD_FAST                'value'
              240  CALL_METHOD_1         1  '1 positional argument'
          242_244  POP_JUMP_IF_FALSE   272  'to 272'

 L.  74       246  LOAD_GLOBAL              w
              248  LOAD_ATTR                ard
              250  LOAD_METHOD              set_pin_mode
              252  LOAD_GLOBAL              w
              254  LOAD_METHOD              p
              256  LOAD_FAST                'pin'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  LOAD_GLOBAL              w
              262  LOAD_ATTR                Constants
              264  LOAD_ATTR                PULLUP
              266  CALL_METHOD_2         2  '2 positional arguments'
              268  POP_TOP          
              270  JUMP_FORWARD        778  'to 778'
            272_0  COME_FROM           242  '242'

 L.  76       272  LOAD_GLOBAL              w
              274  LOAD_ATTR                log
              276  LOAD_METHOD              error
              278  LOAD_FAST                'value'
              280  LOAD_STR                 'arg'
              282  CALL_METHOD_2         2  '2 positional arguments'
              284  POP_TOP          
          286_288  JUMP_FORWARD        778  'to 778'
            290_0  COME_FROM           158  '158'

 L.  78       290  LOAD_GLOBAL              w
              292  LOAD_METHOD              isA
              294  LOAD_FAST                'pin'
              296  CALL_METHOD_1         1  '1 positional argument'
          298_300  POP_JUMP_IF_FALSE   428  'to 428'

 L.  79       302  LOAD_GLOBAL              w
              304  LOAD_METHOD              isOutput
              306  LOAD_FAST                'value'
              308  CALL_METHOD_1         1  '1 positional argument'
          310_312  POP_JUMP_IF_FALSE   334  'to 334'

 L.  80       314  LOAD_GLOBAL              w
              316  LOAD_ATTR                log
              318  LOAD_METHOD              error
              320  LOAD_STR                 'Analog pin {0} cannot be set as OUTPUT'
              322  LOAD_METHOD              format
              324  LOAD_FAST                'pin'
              326  CALL_METHOD_1         1  '1 positional argument'
              328  CALL_METHOD_1         1  '1 positional argument'
              330  POP_TOP          
              332  JUMP_FORWARD        778  'to 778'
            334_0  COME_FROM           310  '310'

 L.  81       334  LOAD_GLOBAL              w
              336  LOAD_METHOD              isInput
              338  LOAD_FAST                'value'
              340  CALL_METHOD_1         1  '1 positional argument'
          342_344  POP_JUMP_IF_FALSE   372  'to 372'

 L.  82       346  LOAD_GLOBAL              w
              348  LOAD_ATTR                ard
              350  LOAD_METHOD              set_pin_mode
              352  LOAD_GLOBAL              w
              354  LOAD_METHOD              p
              356  LOAD_FAST                'pin'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  LOAD_GLOBAL              w
              362  LOAD_ATTR                Constants
              364  LOAD_ATTR                ANALOG
              366  CALL_METHOD_2         2  '2 positional arguments'
              368  POP_TOP          
              370  JUMP_FORWARD        778  'to 778'
            372_0  COME_FROM           342  '342'

 L.  83       372  LOAD_GLOBAL              w
              374  LOAD_METHOD              isPullupInput
              376  LOAD_FAST                'value'
              378  CALL_METHOD_1         1  '1 positional argument'
          380_382  POP_JUMP_IF_FALSE   410  'to 410'

 L.  84       384  LOAD_GLOBAL              w
              386  LOAD_ATTR                ard
              388  LOAD_METHOD              set_pin_mode
              390  LOAD_GLOBAL              w
              392  LOAD_METHOD              p
              394  LOAD_FAST                'pin'
              396  CALL_METHOD_1         1  '1 positional argument'
              398  LOAD_GLOBAL              w
              400  LOAD_ATTR                Constants
              402  LOAD_ATTR                PULLUP
              404  CALL_METHOD_2         2  '2 positional arguments'
              406  POP_TOP          
              408  JUMP_FORWARD        778  'to 778'
            410_0  COME_FROM           380  '380'

 L.  86       410  LOAD_GLOBAL              w
              412  LOAD_ATTR                log
              414  LOAD_METHOD              error
              416  LOAD_FAST                'value'
              418  LOAD_STR                 'arg'
              420  CALL_METHOD_2         2  '2 positional arguments'
              422  POP_TOP          
          424_426  JUMP_FORWARD        778  'to 778'
            428_0  COME_FROM           298  '298'

 L.  88       428  LOAD_GLOBAL              w
              430  LOAD_METHOD              isAdig
              432  LOAD_FAST                'pin'
              434  CALL_METHOD_1         1  '1 positional argument'
          436_438  POP_JUMP_IF_FALSE   570  'to 570'

 L.  89       440  LOAD_GLOBAL              w
              442  LOAD_METHOD              isOutput
              444  LOAD_FAST                'value'
              446  CALL_METHOD_1         1  '1 positional argument'
          448_450  POP_JUMP_IF_FALSE   478  'to 478'

 L.  90       452  LOAD_GLOBAL              w
              454  LOAD_ATTR                ard
              456  LOAD_METHOD              set_pin_mode
              458  LOAD_GLOBAL              w
              460  LOAD_METHOD              p
              462  LOAD_FAST                'pin'
              464  CALL_METHOD_1         1  '1 positional argument'
              466  LOAD_GLOBAL              w
              468  LOAD_ATTR                Constants
              470  LOAD_ATTR                OUTPUT
              472  CALL_METHOD_2         2  '2 positional arguments'
              474  POP_TOP          
              476  JUMP_FORWARD        568  'to 568'
            478_0  COME_FROM           448  '448'

 L.  91       478  LOAD_GLOBAL              w
              480  LOAD_METHOD              isInput
              482  LOAD_FAST                'value'
              484  CALL_METHOD_1         1  '1 positional argument'
          486_488  POP_JUMP_IF_FALSE   516  'to 516'

 L.  92       490  LOAD_GLOBAL              w
              492  LOAD_ATTR                ard
              494  LOAD_METHOD              set_pin_mode
              496  LOAD_GLOBAL              w
              498  LOAD_METHOD              p
              500  LOAD_FAST                'pin'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  LOAD_GLOBAL              w
              506  LOAD_ATTR                Constants
              508  LOAD_ATTR                INPUT
              510  CALL_METHOD_2         2  '2 positional arguments'
              512  POP_TOP          
              514  JUMP_FORWARD        568  'to 568'
            516_0  COME_FROM           486  '486'

 L.  93       516  LOAD_GLOBAL              w
              518  LOAD_METHOD              isPullupInput
              520  LOAD_FAST                'value'
              522  CALL_METHOD_1         1  '1 positional argument'
          524_526  POP_JUMP_IF_FALSE   554  'to 554'

 L.  94       528  LOAD_GLOBAL              w
              530  LOAD_ATTR                ard
              532  LOAD_METHOD              set_pin_mode
              534  LOAD_GLOBAL              w
              536  LOAD_METHOD              p
              538  LOAD_FAST                'pin'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  LOAD_GLOBAL              w
              544  LOAD_ATTR                Constants
              546  LOAD_ATTR                PULLUP
              548  CALL_METHOD_2         2  '2 positional arguments'
              550  POP_TOP          
              552  JUMP_FORWARD        568  'to 568'
            554_0  COME_FROM           524  '524'

 L.  96       554  LOAD_GLOBAL              w
              556  LOAD_ATTR                log
              558  LOAD_METHOD              error
              560  LOAD_FAST                'value'
              562  LOAD_STR                 'arg'
              564  CALL_METHOD_2         2  '2 positional arguments'
              566  POP_TOP          
            568_0  COME_FROM           552  '552'
            568_1  COME_FROM           514  '514'
            568_2  COME_FROM           476  '476'
              568  JUMP_FORWARD        778  'to 778'
            570_0  COME_FROM           436  '436'

 L.  98       570  LOAD_GLOBAL              w
              572  LOAD_METHOD              isButton
              574  LOAD_FAST                'pin'
              576  CALL_METHOD_1         1  '1 positional argument'
          578_580  POP_JUMP_IF_FALSE   658  'to 658'

 L.  99       582  LOAD_GLOBAL              w
              584  LOAD_METHOD              isOutput
              586  LOAD_FAST                'value'
              588  CALL_METHOD_1         1  '1 positional argument'
          590_592  POP_JUMP_IF_FALSE   614  'to 614'

 L. 100       594  LOAD_GLOBAL              w
              596  LOAD_ATTR                log
              598  LOAD_METHOD              error
              600  LOAD_STR                 'Button pin {0} cannot be set as OUTPUT'
              602  LOAD_METHOD              format
              604  LOAD_FAST                'pin'
              606  CALL_METHOD_1         1  '1 positional argument'
              608  CALL_METHOD_1         1  '1 positional argument'
              610  POP_TOP          
              612  JUMP_FORWARD        656  'to 656'
            614_0  COME_FROM           590  '590'

 L. 101       614  LOAD_GLOBAL              w
              616  LOAD_METHOD              isInput
              618  LOAD_FAST                'value'
              620  CALL_METHOD_1         1  '1 positional argument'
          622_624  POP_JUMP_IF_FALSE   628  'to 628'

 L. 102       626  JUMP_FORWARD        656  'to 656'
            628_0  COME_FROM           622  '622'

 L. 103       628  LOAD_GLOBAL              w
              630  LOAD_METHOD              isPullupInput
              632  LOAD_FAST                'value'
              634  CALL_METHOD_1         1  '1 positional argument'
          636_638  POP_JUMP_IF_FALSE   642  'to 642'

 L. 104       640  JUMP_FORWARD        656  'to 656'
            642_0  COME_FROM           636  '636'

 L. 106       642  LOAD_GLOBAL              w
              644  LOAD_ATTR                log
              646  LOAD_METHOD              error
              648  LOAD_FAST                'value'
              650  LOAD_STR                 'arg'
              652  CALL_METHOD_2         2  '2 positional arguments'
              654  POP_TOP          
            656_0  COME_FROM           640  '640'
            656_1  COME_FROM           626  '626'
            656_2  COME_FROM           612  '612'
              656  JUMP_FORWARD        778  'to 778'
            658_0  COME_FROM           578  '578'

 L. 108       658  LOAD_GLOBAL              w
              660  LOAD_METHOD              isLED
              662  LOAD_FAST                'pin'
              664  CALL_METHOD_1         1  '1 positional argument'
          666_668  POP_JUMP_IF_FALSE   764  'to 764'

 L. 109       670  LOAD_GLOBAL              w
              672  LOAD_METHOD              isOutput
              674  LOAD_FAST                'value'
              676  CALL_METHOD_1         1  '1 positional argument'
          678_680  POP_JUMP_IF_FALSE   684  'to 684'

 L. 110       682  JUMP_FORWARD        762  'to 762'
            684_0  COME_FROM           678  '678'
            684_1  COME_FROM           332  '332'

 L. 111       684  LOAD_GLOBAL              w
            686_0  COME_FROM           196  '196'
              686  LOAD_METHOD              isInput
            688_0  COME_FROM            58  '58'
              688  LOAD_FAST                'value'
              690  CALL_METHOD_1         1  '1 positional argument'
          692_694  POP_JUMP_IF_FALSE   716  'to 716'

 L. 112       696  LOAD_GLOBAL              w
              698  LOAD_ATTR                log
              700  LOAD_METHOD              error
              702  LOAD_STR                 'LED pin {0} cannot be set as INPUT'
              704  LOAD_METHOD              format
              706  LOAD_FAST                'pin'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  CALL_METHOD_1         1  '1 positional argument'
              712  POP_TOP          
              714  JUMP_FORWARD        762  'to 762'
            716_0  COME_FROM           692  '692'

 L. 113       716  LOAD_GLOBAL              w
              718  LOAD_METHOD              isPullupInput
              720  LOAD_FAST                'value'
            722_0  COME_FROM           370  '370'
            722_1  COME_FROM           232  '232'
              722  CALL_METHOD_1         1  '1 positional argument'
            724_0  COME_FROM            94  '94'
          724_726  POP_JUMP_IF_FALSE   748  'to 748'

 L. 114       728  LOAD_GLOBAL              w
              730  LOAD_ATTR                log
              732  LOAD_METHOD              error
              734  LOAD_STR                 'LED pin {0} cannot be set as INPUT'
              736  LOAD_METHOD              format
              738  LOAD_FAST                'pin'
              740  CALL_METHOD_1         1  '1 positional argument'
              742  CALL_METHOD_1         1  '1 positional argument'
              744  POP_TOP          
              746  JUMP_FORWARD        762  'to 762'
            748_0  COME_FROM           724  '724'

 L. 116       748  LOAD_GLOBAL              w
              750  LOAD_ATTR                log
              752  LOAD_METHOD              error
              754  LOAD_FAST                'value'
              756  LOAD_STR                 'arg'
              758  CALL_METHOD_2         2  '2 positional arguments'
            760_0  COME_FROM           408  '408'
            760_1  COME_FROM           270  '270'
            760_2  COME_FROM           130  '130'
              760  POP_TOP          
            762_0  COME_FROM           746  '746'
            762_1  COME_FROM           714  '714'
            762_2  COME_FROM           682  '682'
              762  JUMP_FORWARD        778  'to 778'
            764_0  COME_FROM           666  '666'

 L. 119       764  LOAD_GLOBAL              w
              766  LOAD_ATTR                log
              768  LOAD_METHOD              error
              770  LOAD_FAST                'pin'
              772  LOAD_STR                 'arg'
              774  CALL_METHOD_2         2  '2 positional arguments'
              776  POP_TOP          
            778_0  COME_FROM           762  '762'
            778_1  COME_FROM           656  '656'
            778_2  COME_FROM           568  '568'
            778_3  COME_FROM           424  '424'
            778_4  COME_FROM           286  '286'
            778_5  COME_FROM           146  '146'
            778_6  COME_FROM            10  '10'

 L. 121       778  LOAD_GLOBAL              w
              780  LOAD_METHOD              transformMode
              782  LOAD_FAST                'value'
              784  CALL_METHOD_1         1  '1 positional argument'
              786  STORE_FAST               'm'

 L. 122       788  LOAD_FAST                'm'
              790  LOAD_CONST               None
              792  COMPARE_OP               !=
          794_796  POP_JUMP_IF_FALSE   808  'to 808'

 L. 123       798  LOAD_FAST                'm'
              800  LOAD_GLOBAL              w
              802  LOAD_ATTR                pinState
              804  LOAD_FAST                'pin'
              806  STORE_SUBSCR     
            808_0  COME_FROM           794  '794'

Parse error at or near `COME_FROM' instruction at offset 686_0


def digitalWrite--- This code section failed: ---

 L. 128         0  LOAD_GLOBAL              w
                2  LOAD_METHOD              isR
                4  LOAD_FAST                'pin'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_FALSE   162  'to 162'

 L. 129        10  LOAD_GLOBAL              w
               12  LOAD_METHOD              isPinOutput
               14  LOAD_FAST                'pin'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_JUMP_IF_FALSE   140  'to 140'

 L. 130        20  LOAD_GLOBAL              w
               22  LOAD_METHOD              isLow
               24  LOAD_FAST                'value'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  POP_JUMP_IF_FALSE    72  'to 72'

 L. 131        30  LOAD_GLOBAL              w
               32  LOAD_ATTR                rpi
               34  LOAD_ATTR                OutputDevice
               36  LOAD_GLOBAL              w
               38  LOAD_METHOD              p
               40  LOAD_FAST                'pin'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  LOAD_GLOBAL              w
               46  LOAD_ATTR                defaultFactory
               48  LOAD_CONST               ('pin_factory',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  STORE_FAST               'x'

 L. 132        54  LOAD_FAST                'x'
               56  LOAD_METHOD              off
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  POP_TOP          

 L. 133        62  LOAD_FAST                'x'
               64  LOAD_METHOD              close
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  POP_TOP          
               70  JUMP_ABSOLUTE       158  'to 158'
             72_0  COME_FROM            28  '28'

 L. 134        72  LOAD_GLOBAL              w
               74  LOAD_METHOD              isHigh
               76  LOAD_FAST                'value'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  POP_JUMP_IF_FALSE   124  'to 124'

 L. 135        82  LOAD_GLOBAL              w
               84  LOAD_ATTR                rpi
               86  LOAD_ATTR                OutputDevice
               88  LOAD_GLOBAL              w
               90  LOAD_METHOD              p
               92  LOAD_FAST                'pin'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  LOAD_GLOBAL              w
               98  LOAD_ATTR                defaultFactory
              100  LOAD_CONST               ('pin_factory',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  STORE_FAST               'x'

 L. 136       106  LOAD_FAST                'x'
              108  LOAD_METHOD              on
              110  CALL_METHOD_0         0  '0 positional arguments'
              112  POP_TOP          

 L. 137       114  LOAD_FAST                'x'
              116  LOAD_METHOD              close
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  POP_TOP          
              122  JUMP_ABSOLUTE       158  'to 158'
            124_0  COME_FROM            80  '80'

 L. 139       124  LOAD_GLOBAL              w
              126  LOAD_ATTR                log
              128  LOAD_METHOD              error
              130  LOAD_FAST                'value'
              132  LOAD_STR                 'arg'
              134  CALL_METHOD_2         2  '2 positional arguments'
              136  POP_TOP          
              138  JUMP_FORWARD        674  'to 674'
            140_0  COME_FROM            18  '18'

 L. 141       140  LOAD_GLOBAL              w
              142  LOAD_ATTR                log
              144  LOAD_METHOD              error
              146  LOAD_STR                 'Raspberry pin {0} must be set as OUTPUT for digitalWrite'
              148  LOAD_METHOD              format
              150  LOAD_FAST                'pin'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          
          158_160  JUMP_FORWARD        674  'to 674'
            162_0  COME_FROM             8  '8'

 L. 143       162  LOAD_GLOBAL              w
              164  LOAD_METHOD              isDPWM
              166  LOAD_FAST                'pin'
              168  CALL_METHOD_1         1  '1 positional argument'
          170_172  POP_JUMP_IF_FALSE   288  'to 288'

 L. 144       174  LOAD_GLOBAL              w
              176  LOAD_METHOD              isPinOutput
              178  LOAD_FAST                'pin'
              180  CALL_METHOD_1         1  '1 positional argument'
          182_184  POP_JUMP_IF_FALSE   266  'to 266'

 L. 145       186  LOAD_GLOBAL              w
              188  LOAD_METHOD              isLow
              190  LOAD_FAST                'value'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_JUMP_IF_FALSE   218  'to 218'

 L. 146       196  LOAD_GLOBAL              w
              198  LOAD_ATTR                ard
              200  LOAD_METHOD              analog_write
              202  LOAD_GLOBAL              w
              204  LOAD_METHOD              p
              206  LOAD_FAST                'pin'
              208  CALL_METHOD_1         1  '1 positional argument'
              210  LOAD_CONST               0
              212  CALL_METHOD_2         2  '2 positional arguments'
              214  POP_TOP          
              216  JUMP_FORWARD        264  'to 264'
            218_0  COME_FROM           194  '194'

 L. 147       218  LOAD_GLOBAL              w
              220  LOAD_METHOD              isHigh
              222  LOAD_FAST                'value'
              224  CALL_METHOD_1         1  '1 positional argument'
              226  POP_JUMP_IF_FALSE   250  'to 250'

 L. 148       228  LOAD_GLOBAL              w
              230  LOAD_ATTR                ard
              232  LOAD_METHOD              analog_write
              234  LOAD_GLOBAL              w
              236  LOAD_METHOD              p
              238  LOAD_FAST                'pin'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  LOAD_CONST               255
              244  CALL_METHOD_2         2  '2 positional arguments'
              246  POP_TOP          
              248  JUMP_FORWARD        264  'to 264'
            250_0  COME_FROM           226  '226'

 L. 150       250  LOAD_GLOBAL              w
              252  LOAD_ATTR                log
              254  LOAD_METHOD              error
              256  LOAD_FAST                'value'
              258  LOAD_STR                 'arg'
              260  CALL_METHOD_2         2  '2 positional arguments'
              262  POP_TOP          
            264_0  COME_FROM           248  '248'
            264_1  COME_FROM           216  '216'
              264  JUMP_FORWARD        674  'to 674'
            266_0  COME_FROM           182  '182'

 L. 152       266  LOAD_GLOBAL              w
              268  LOAD_ATTR                log
              270  LOAD_METHOD              error
              272  LOAD_STR                 'Pin {0} must be set as OUTPUT for digitalWrite'
              274  LOAD_METHOD              format
              276  LOAD_FAST                'pin'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          
          284_286  JUMP_FORWARD        674  'to 674'
            288_0  COME_FROM           170  '170'

 L. 154       288  LOAD_GLOBAL              w
              290  LOAD_METHOD              isD
              292  LOAD_FAST                'pin'
              294  CALL_METHOD_1         1  '1 positional argument'
          296_298  POP_JUMP_IF_TRUE    312  'to 312'
              300  LOAD_GLOBAL              w
              302  LOAD_METHOD              isAdig
              304  LOAD_FAST                'pin'
              306  CALL_METHOD_1         1  '1 positional argument'
          308_310  POP_JUMP_IF_FALSE   428  'to 428'
            312_0  COME_FROM           296  '296'

 L. 155       312  LOAD_GLOBAL              w
              314  LOAD_METHOD              isPinOutput
              316  LOAD_FAST                'pin'
              318  CALL_METHOD_1         1  '1 positional argument'
          320_322  POP_JUMP_IF_FALSE   408  'to 408'

 L. 156       324  LOAD_GLOBAL              w
              326  LOAD_METHOD              isLow
              328  LOAD_FAST                'value'
              330  CALL_METHOD_1         1  '1 positional argument'
          332_334  POP_JUMP_IF_FALSE   358  'to 358'

 L. 157       336  LOAD_GLOBAL              w
              338  LOAD_ATTR                ard
              340  LOAD_METHOD              digital_write
              342  LOAD_GLOBAL              w
              344  LOAD_METHOD              p
              346  LOAD_FAST                'pin'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  LOAD_CONST               0
              352  CALL_METHOD_2         2  '2 positional arguments'
              354  POP_TOP          
              356  JUMP_FORWARD        406  'to 406'
            358_0  COME_FROM           332  '332'

 L. 158       358  LOAD_GLOBAL              w
              360  LOAD_METHOD              isHigh
              362  LOAD_FAST                'value'
              364  CALL_METHOD_1         1  '1 positional argument'
          366_368  POP_JUMP_IF_FALSE   392  'to 392'

 L. 159       370  LOAD_GLOBAL              w
              372  LOAD_ATTR                ard
              374  LOAD_METHOD              digital_write
              376  LOAD_GLOBAL              w
              378  LOAD_METHOD              p
              380  LOAD_FAST                'pin'
              382  CALL_METHOD_1         1  '1 positional argument'
              384  LOAD_CONST               1
              386  CALL_METHOD_2         2  '2 positional arguments'
              388  POP_TOP          
              390  JUMP_FORWARD        406  'to 406'
            392_0  COME_FROM           366  '366'

 L. 161       392  LOAD_GLOBAL              w
              394  LOAD_ATTR                log
              396  LOAD_METHOD              error
              398  LOAD_FAST                'value'
              400  LOAD_STR                 'arg'
              402  CALL_METHOD_2         2  '2 positional arguments'
              404  POP_TOP          
            406_0  COME_FROM           390  '390'
            406_1  COME_FROM           356  '356'
              406  JUMP_FORWARD        426  'to 426'
            408_0  COME_FROM           320  '320'

 L. 163       408  LOAD_GLOBAL              w
              410  LOAD_ATTR                log
              412  LOAD_METHOD              error
              414  LOAD_STR                 'Pin {0} must be set as OUTPUT for digitalWrite'
              416  LOAD_METHOD              format
              418  LOAD_FAST                'pin'
              420  CALL_METHOD_1         1  '1 positional argument'
              422  CALL_METHOD_1         1  '1 positional argument'
              424  POP_TOP          
            426_0  COME_FROM           406  '406'
              426  JUMP_FORWARD        674  'to 674'
            428_0  COME_FROM           308  '308'

 L. 165       428  LOAD_GLOBAL              w
              430  LOAD_METHOD              isA
              432  LOAD_FAST                'pin'
              434  CALL_METHOD_1         1  '1 positional argument'
          436_438  POP_JUMP_IF_FALSE   460  'to 460'

 L. 166       440  LOAD_GLOBAL              w
              442  LOAD_ATTR                log
              444  LOAD_METHOD              error
              446  LOAD_STR                 'Analog pin {0} cannot be used for digitalWrite'
              448  LOAD_METHOD              format
              450  LOAD_FAST                'pin'
              452  CALL_METHOD_1         1  '1 positional argument'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  POP_TOP          
              458  JUMP_FORWARD        674  'to 674'
            460_0  COME_FROM           436  '436'

 L. 168       460  LOAD_GLOBAL              w
              462  LOAD_METHOD              isButton
              464  LOAD_FAST                'pin'
              466  CALL_METHOD_1         1  '1 positional argument'
          468_470  POP_JUMP_IF_FALSE   492  'to 492'

 L. 169       472  LOAD_GLOBAL              w
              474  LOAD_ATTR                log
              476  LOAD_METHOD              error
              478  LOAD_STR                 'Button pin {0} cannot be used for digitalWrite'
              480  LOAD_METHOD              format
              482  LOAD_FAST                'pin'
              484  CALL_METHOD_1         1  '1 positional argument'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  POP_TOP          
              490  JUMP_FORWARD        674  'to 674'
            492_0  COME_FROM           468  '468'

 L. 171       492  LOAD_GLOBAL              w
              494  LOAD_METHOD              isLED
              496  LOAD_FAST                'pin'
              498  CALL_METHOD_1         1  '1 positional argument'
          500_502  POP_JUMP_IF_FALSE   660  'to 660'

 L. 172       504  LOAD_GLOBAL              w
              506  LOAD_METHOD              isPinOutput
              508  LOAD_FAST                'pin'
              510  CALL_METHOD_1         1  '1 positional argument'
          512_514  POP_JUMP_IF_FALSE   640  'to 640'

 L. 173       516  LOAD_GLOBAL              w
              518  LOAD_METHOD              isLow
              520  LOAD_FAST                'value'
              522  CALL_METHOD_1         1  '1 positional argument'
          524_526  POP_JUMP_IF_FALSE   570  'to 570'

 L. 174       528  LOAD_GLOBAL              w
              530  LOAD_ATTR                rpi
              532  LOAD_ATTR                OutputDevice
              534  LOAD_GLOBAL              w
              536  LOAD_METHOD              p
              538  LOAD_FAST                'pin'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  LOAD_GLOBAL              w
              544  LOAD_ATTR                defaultFactory
              546  LOAD_CONST               ('pin_factory',)
              548  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              550  STORE_FAST               'x'

 L. 175       552  LOAD_FAST                'x'
              554  LOAD_METHOD              off
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  POP_TOP          

 L. 176       560  LOAD_FAST                'x'
              562  LOAD_METHOD              close
              564  CALL_METHOD_0         0  '0 positional arguments'
              566  POP_TOP          
              568  JUMP_FORWARD        638  'to 638'
            570_0  COME_FROM           524  '524'

 L. 177       570  LOAD_GLOBAL              w
              572  LOAD_METHOD              isHigh
              574  LOAD_FAST                'value'
              576  CALL_METHOD_1         1  '1 positional argument'
          578_580  POP_JUMP_IF_FALSE   624  'to 624'

 L. 178       582  LOAD_GLOBAL              w
              584  LOAD_ATTR                rpi
              586  LOAD_ATTR                OutputDevice
              588  LOAD_GLOBAL              w
              590  LOAD_METHOD              p
              592  LOAD_FAST                'pin'
              594  CALL_METHOD_1         1  '1 positional argument'
              596  LOAD_GLOBAL              w
              598  LOAD_ATTR                defaultFactory
              600  LOAD_CONST               ('pin_factory',)
              602  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              604  STORE_FAST               'x'

 L. 179       606  LOAD_FAST                'x'
              608  LOAD_METHOD              on
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  POP_TOP          

 L. 180       614  LOAD_FAST                'x'
              616  LOAD_METHOD              close
              618  CALL_METHOD_0         0  '0 positional arguments'
              620  POP_TOP          
              622  JUMP_FORWARD        638  'to 638'
            624_0  COME_FROM           578  '578'

 L. 182       624  LOAD_GLOBAL              w
              626  LOAD_ATTR                log
              628  LOAD_METHOD              error
              630  LOAD_FAST                'value'
              632  LOAD_STR                 'arg'
              634  CALL_METHOD_2         2  '2 positional arguments'
              636  POP_TOP          
            638_0  COME_FROM           622  '622'
            638_1  COME_FROM           568  '568'
              638  JUMP_FORWARD        658  'to 658'
            640_0  COME_FROM           512  '512'

 L. 184       640  LOAD_GLOBAL              w
              642  LOAD_ATTR                log
              644  LOAD_METHOD              error
              646  LOAD_STR                 'LED pin {0} must be set as OUTPUT for digitalWrite'
              648  LOAD_METHOD              format
              650  LOAD_FAST                'pin'
            652_0  COME_FROM           264  '264'
            652_1  COME_FROM           138  '138'
              652  CALL_METHOD_1         1  '1 positional argument'
              654  CALL_METHOD_1         1  '1 positional argument'
              656  POP_TOP          
            658_0  COME_FROM           638  '638'
              658  JUMP_FORWARD        674  'to 674'
            660_0  COME_FROM           500  '500'

 L. 187       660  LOAD_GLOBAL              w
              662  LOAD_ATTR                log
              664  LOAD_METHOD              error
              666  LOAD_FAST                'pin'
              668  LOAD_STR                 'arg'
              670  CALL_METHOD_2         2  '2 positional arguments'
              672  POP_TOP          
            674_0  COME_FROM           658  '658'
            674_1  COME_FROM           490  '490'
            674_2  COME_FROM           458  '458'
            674_3  COME_FROM           426  '426'
            674_4  COME_FROM           284  '284'
            674_5  COME_FROM           158  '158'

Parse error at or near `COME_FROM' instruction at offset 652_0


def digitalRead--- This code section failed: ---

 L. 192         0  LOAD_GLOBAL              w
                2  LOAD_METHOD              isR
                4  LOAD_FAST                'pin'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_FALSE   160  'to 160'

 L. 193        10  LOAD_GLOBAL              w
               12  LOAD_METHOD              isPinInput
               14  LOAD_FAST                'pin'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_JUMP_IF_FALSE    74  'to 74'

 L. 194        20  LOAD_GLOBAL              w
               22  LOAD_ATTR                rpi
               24  LOAD_ATTR                InputDevice
               26  LOAD_GLOBAL              w
               28  LOAD_METHOD              p
               30  LOAD_FAST                'pin'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  LOAD_CONST               False
               36  LOAD_GLOBAL              w
               38  LOAD_ATTR                defaultFactory
               40  LOAD_CONST               ('pin_factory',)
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  STORE_FAST               'x'

 L. 195        46  LOAD_FAST                'x'
               48  LOAD_ATTR                value
               50  STORE_FAST               'v'

 L. 196        52  LOAD_FAST                'x'
               54  LOAD_METHOD              close
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  POP_TOP          

 L. 197        60  LOAD_FAST                'v'
               62  POP_JUMP_IF_FALSE    68  'to 68'

 L. 197        64  LOAD_CONST               1
               66  RETURN_VALUE     
             68_0  COME_FROM            62  '62'

 L. 198        68  LOAD_CONST               0
               70  RETURN_VALUE     
               72  JUMP_FORWARD        456  'to 456'
             74_0  COME_FROM            18  '18'

 L. 199        74  LOAD_GLOBAL              w
               76  LOAD_METHOD              isPinPullupInput
               78  LOAD_FAST                'pin'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  POP_JUMP_IF_FALSE   138  'to 138'

 L. 200        84  LOAD_GLOBAL              w
               86  LOAD_ATTR                rpi
               88  LOAD_ATTR                InputDevice
               90  LOAD_GLOBAL              w
               92  LOAD_METHOD              p
               94  LOAD_FAST                'pin'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  LOAD_CONST               True
              100  LOAD_GLOBAL              w
              102  LOAD_ATTR                defaultFactory
              104  LOAD_CONST               ('pin_factory',)
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  STORE_FAST               'x'

 L. 201       110  LOAD_FAST                'x'
              112  LOAD_ATTR                value
              114  STORE_FAST               'v'

 L. 202       116  LOAD_FAST                'x'
              118  LOAD_METHOD              close
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  POP_TOP          

 L. 203       124  LOAD_FAST                'v'
              126  POP_JUMP_IF_FALSE   132  'to 132'

 L. 203       128  LOAD_CONST               1
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'

 L. 204       132  LOAD_CONST               0
              134  RETURN_VALUE     
              136  JUMP_FORWARD        456  'to 456'
            138_0  COME_FROM            82  '82'

 L. 206       138  LOAD_GLOBAL              w
              140  LOAD_ATTR                log
              142  LOAD_METHOD              error
              144  LOAD_STR                 'Raspberry pin {0} must be set as INPUT for digitalRead'
              146  LOAD_METHOD              format
              148  LOAD_FAST                'pin'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          
          156_158  JUMP_FORWARD        456  'to 456'
            160_0  COME_FROM             8  '8'

 L. 208       160  LOAD_GLOBAL              w
              162  LOAD_METHOD              isD
              164  LOAD_FAST                'pin'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_JUMP_IF_TRUE    180  'to 180'
              170  LOAD_GLOBAL              w
              172  LOAD_METHOD              isAdig
              174  LOAD_FAST                'pin'
              176  CALL_METHOD_1         1  '1 positional argument'
              178  POP_JUMP_IF_FALSE   212  'to 212'
            180_0  COME_FROM           168  '168'

 L. 209       180  LOAD_GLOBAL              w
              182  LOAD_ATTR                ard
              184  LOAD_METHOD              digital_read
              186  LOAD_GLOBAL              w
              188  LOAD_METHOD              p
              190  LOAD_FAST                'pin'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  CALL_METHOD_1         1  '1 positional argument'
              196  STORE_FAST               'v'

 L. 210       198  LOAD_FAST                'v'
              200  POP_JUMP_IF_FALSE   206  'to 206'

 L. 210       202  LOAD_CONST               1
              204  RETURN_VALUE     
            206_0  COME_FROM           200  '200'

 L. 211       206  LOAD_CONST               0
              208  RETURN_VALUE     
              210  JUMP_FORWARD        456  'to 456'
            212_0  COME_FROM           178  '178'

 L. 213       212  LOAD_GLOBAL              w
              214  LOAD_METHOD              isA
              216  LOAD_FAST                'pin'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_JUMP_IF_FALSE   242  'to 242'

 L. 214       222  LOAD_GLOBAL              w
              224  LOAD_ATTR                log
              226  LOAD_METHOD              error
              228  LOAD_STR                 'Analog pin {0} cannot be used for digitalRead'
              230  LOAD_METHOD              format
              232  LOAD_FAST                'pin'
              234  CALL_METHOD_1         1  '1 positional argument'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  POP_TOP          
              240  JUMP_FORWARD        456  'to 456'
            242_0  COME_FROM           220  '220'

 L. 216       242  LOAD_GLOBAL              w
              244  LOAD_METHOD              isButton
              246  LOAD_FAST                'pin'
              248  CALL_METHOD_1         1  '1 positional argument'
          250_252  POP_JUMP_IF_FALSE   410  'to 410'

 L. 217       254  LOAD_GLOBAL              w
              256  LOAD_METHOD              isPinInput
              258  LOAD_FAST                'pin'
              260  CALL_METHOD_1         1  '1 positional argument'
          262_264  POP_JUMP_IF_FALSE   322  'to 322'

 L. 218       266  LOAD_GLOBAL              w
              268  LOAD_ATTR                rpi
              270  LOAD_ATTR                InputDevice
              272  LOAD_GLOBAL              w
              274  LOAD_METHOD              p
              276  LOAD_FAST                'pin'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  LOAD_CONST               False
              282  LOAD_GLOBAL              w
              284  LOAD_ATTR                defaultFactory
              286  LOAD_CONST               ('pin_factory',)
              288  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              290  STORE_FAST               'x'

 L. 219       292  LOAD_FAST                'x'
              294  LOAD_ATTR                value
              296  STORE_FAST               'v'

 L. 220       298  LOAD_FAST                'x'
              300  LOAD_METHOD              close
              302  CALL_METHOD_0         0  '0 positional arguments'
              304  POP_TOP          

 L. 221       306  LOAD_FAST                'v'
          308_310  POP_JUMP_IF_FALSE   316  'to 316'

 L. 221       312  LOAD_CONST               1
              314  RETURN_VALUE     
            316_0  COME_FROM           308  '308'

 L. 222       316  LOAD_CONST               0
              318  RETURN_VALUE     
              320  JUMP_FORWARD        408  'to 408'
            322_0  COME_FROM           262  '262'

 L. 223       322  LOAD_GLOBAL              w
              324  LOAD_METHOD              isPinPullupInput
              326  LOAD_FAST                'pin'
              328  CALL_METHOD_1         1  '1 positional argument'
          330_332  POP_JUMP_IF_FALSE   390  'to 390'

 L. 224       334  LOAD_GLOBAL              w
              336  LOAD_ATTR                rpi
              338  LOAD_ATTR                InputDevice
              340  LOAD_GLOBAL              w
              342  LOAD_METHOD              p
              344  LOAD_FAST                'pin'
              346  CALL_METHOD_1         1  '1 positional argument'
              348  LOAD_CONST               True
              350  LOAD_GLOBAL              w
              352  LOAD_ATTR                defaultFactory
              354  LOAD_CONST               ('pin_factory',)
              356  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              358  STORE_FAST               'x'

 L. 225       360  LOAD_FAST                'x'
              362  LOAD_ATTR                value
              364  STORE_FAST               'v'

 L. 226       366  LOAD_FAST                'x'
              368  LOAD_METHOD              close
            370_0  COME_FROM            72  '72'
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  POP_TOP          

 L. 227       374  LOAD_FAST                'v'
          376_378  POP_JUMP_IF_FALSE   384  'to 384'

 L. 227       380  LOAD_CONST               1
              382  RETURN_VALUE     
            384_0  COME_FROM           376  '376'

 L. 228       384  LOAD_CONST               0
              386  RETURN_VALUE     
              388  JUMP_FORWARD        408  'to 408'
            390_0  COME_FROM           330  '330'

 L. 230       390  LOAD_GLOBAL              w
              392  LOAD_ATTR                log
              394  LOAD_METHOD              error
              396  LOAD_STR                 'Button pin {0} must be set as INPUT for digitalRead'
              398  LOAD_METHOD              format
              400  LOAD_FAST                'pin'
              402  CALL_METHOD_1         1  '1 positional argument'
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          
            408_0  COME_FROM           388  '388'
            408_1  COME_FROM           320  '320'
              408  JUMP_FORWARD        456  'to 456'
            410_0  COME_FROM           250  '250'

 L. 232       410  LOAD_GLOBAL              w
              412  LOAD_METHOD              isLED
              414  LOAD_FAST                'pin'
              416  CALL_METHOD_1         1  '1 positional argument'
          418_420  POP_JUMP_IF_FALSE   442  'to 442'

 L. 233       422  LOAD_GLOBAL              w
              424  LOAD_ATTR                log
              426  LOAD_METHOD              error
              428  LOAD_STR                 'LED pin {0} cannot be used for digitalRead'
              430  LOAD_METHOD              format
              432  LOAD_FAST                'pin'
            434_0  COME_FROM           136  '136'
              434  CALL_METHOD_1         1  '1 positional argument'
              436  CALL_METHOD_1         1  '1 positional argument'
              438  POP_TOP          
              440  JUMP_FORWARD        456  'to 456'
            442_0  COME_FROM           418  '418'

 L. 236       442  LOAD_GLOBAL              w
              444  LOAD_ATTR                log
              446  LOAD_METHOD              error
              448  LOAD_FAST                'pin'
              450  LOAD_STR                 'arg'
              452  CALL_METHOD_2         2  '2 positional arguments'
              454  POP_TOP          
            456_0  COME_FROM           440  '440'
            456_1  COME_FROM           408  '408'
            456_2  COME_FROM           240  '240'
            456_3  COME_FROM           210  '210'
            456_4  COME_FROM           156  '156'

Parse error at or near `COME_FROM' instruction at offset 370_0


def analogRead(pin):
    if w.isR(pin):
        w.log.error('Raspberry pin {0} cannot be used for analogRead'.format(pin))
    else:
        if w.isD(pin) or w.isAdig(pin):
            w.log.error('Digital pin {0} cannot be used for analogRead'.format(pin))
        else:
            if w.isA(pin) and not w.isPinInput(pin):
                if w.isPinPullupInput(pin):
                    return w.ard.analog_read(w.p(pin))
                w.log.error('Analog pin {0} must be set as INPUT for analogRead'.format(pin))
            else:
                if w.isButton(pin):
                    w.log.error('Button pin {0} cannot be used for analogRead'.format(pin))
                else:
                    if w.isLED(pin):
                        w.log.error('LED pin {0} cannot be used for analogRead'.format(pin))
                    else:
                        w.log.errorpin'arg'


def analogWrite--- This code section failed: ---

 L. 261         0  LOAD_GLOBAL              w
                2  LOAD_METHOD              isDPWM
                4  LOAD_FAST                'pin'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_JUMP_IF_FALSE   114  'to 114'

 L. 262        10  LOAD_GLOBAL              w
               12  LOAD_METHOD              isPinOutput
               14  LOAD_FAST                'pin'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_JUMP_IF_FALSE    94  'to 94'

 L. 263        20  LOAD_GLOBAL              int
               22  LOAD_FAST                'value'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  STORE_FAST               'value'

 L. 264        28  LOAD_CONST               0
               30  LOAD_FAST                'value'
               32  DUP_TOP          
               34  ROT_THREE        
               36  COMPARE_OP               <=
               38  POP_JUMP_IF_FALSE    48  'to 48'
               40  LOAD_CONST               255
               42  COMPARE_OP               <=
               44  POP_JUMP_IF_FALSE    74  'to 74'
               46  JUMP_FORWARD         52  'to 52'
             48_0  COME_FROM            38  '38'
               48  POP_TOP          
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM            46  '46'

 L. 265        52  LOAD_GLOBAL              w
               54  LOAD_ATTR                ard
               56  LOAD_METHOD              analog_write
               58  LOAD_GLOBAL              w
               60  LOAD_METHOD              p
               62  LOAD_FAST                'pin'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  LOAD_FAST                'value'
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  POP_TOP          
               72  JUMP_ABSOLUTE       112  'to 112'
             74_0  COME_FROM            50  '50'
             74_1  COME_FROM            44  '44'

 L. 267        74  LOAD_GLOBAL              w
               76  LOAD_ATTR                log
               78  LOAD_METHOD              error
               80  LOAD_STR                 'Argument value "{0}" must be a number between 0 and 255'
               82  LOAD_METHOD              format
               84  LOAD_FAST                'value'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          
               92  JUMP_ABSOLUTE       214  'to 214'
             94_0  COME_FROM            18  '18'

 L. 270        94  LOAD_GLOBAL              w
               96  LOAD_ATTR                log
               98  LOAD_METHOD              error
              100  LOAD_STR                 'Pin {0} must be set as OUTPUT for analogWrite'
              102  LOAD_METHOD              format
              104  LOAD_FAST                'pin'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_TOP          
              112  JUMP_FORWARD        214  'to 214'
            114_0  COME_FROM             8  '8'

 L. 272       114  LOAD_GLOBAL              w
              116  LOAD_METHOD              isD
              118  LOAD_FAST                'pin'
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_JUMP_IF_TRUE    174  'to 174'
              124  LOAD_GLOBAL              w
              126  LOAD_METHOD              isAdig
              128  LOAD_FAST                'pin'
              130  CALL_METHOD_1         1  '1 positional argument'
              132  POP_JUMP_IF_TRUE    174  'to 174'
              134  LOAD_GLOBAL              w
              136  LOAD_METHOD              isR
              138  LOAD_FAST                'pin'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  POP_JUMP_IF_TRUE    174  'to 174'
              144  LOAD_GLOBAL              w
              146  LOAD_METHOD              isA
              148  LOAD_FAST                'pin'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  POP_JUMP_IF_TRUE    174  'to 174'
              154  LOAD_GLOBAL              w
              156  LOAD_METHOD              isButton
              158  LOAD_FAST                'pin'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_JUMP_IF_TRUE    174  'to 174'
              164  LOAD_GLOBAL              w
              166  LOAD_METHOD              isLED
              168  LOAD_FAST                'pin'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  POP_JUMP_IF_FALSE   194  'to 194'
            174_0  COME_FROM           162  '162'
            174_1  COME_FROM           152  '152'
            174_2  COME_FROM           142  '142'
            174_3  COME_FROM           132  '132'
            174_4  COME_FROM           122  '122'

 L. 273       174  LOAD_GLOBAL              w
              176  LOAD_ATTR                log
              178  LOAD_METHOD              error
              180  LOAD_STR                 'Pin {0} cannot be used for analogWrite'
              182  LOAD_METHOD              format
              184  LOAD_FAST                'pin'
              186  CALL_METHOD_1         1  '1 positional argument'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  POP_TOP          
              192  JUMP_FORWARD        214  'to 214'
            194_0  COME_FROM           172  '172'

 L. 276       194  LOAD_GLOBAL              w
              196  LOAD_ATTR                log
              198  LOAD_METHOD              error
              200  LOAD_GLOBAL              w
              202  LOAD_METHOD              p
              204  LOAD_FAST                'pin'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  LOAD_STR                 'arg'
              210  CALL_METHOD_2         2  '2 positional arguments'
              212  POP_TOP          
            214_0  COME_FROM           192  '192'
            214_1  COME_FROM           112  '112'

Parse error at or near `JUMP_FORWARD' instruction at offset 192