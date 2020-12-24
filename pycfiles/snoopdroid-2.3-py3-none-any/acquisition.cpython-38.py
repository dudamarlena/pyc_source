# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/snoopdroid/snoopdroid/acquisition.py
# Compiled at: 2020-04-03 08:08:14
# Size of source mod 2**32: 7756 bytes
import os, sys, json, time, shutil, pkg_resources
from usb1 import USBErrorBusy, USBErrorAccess
from adb import adb_commands
from adb import sign_pythonrsa
from adb.usb_exceptions import DeviceAuthError
from .ui import PullProgress, info, highlight, error
from .utils import get_sha256

class Package(object):

    def __init__(self, name, files=None):
        self.name = name
        self.files = files or []


class Acquisition(object):

    def __init__(self, storage_folder=None, all_apks=False, limit=None, packages=None):
        self.device = None
        self.packages = packages or []
        self.storage_folder = storage_folder
        self.all_apks = all_apks
        self.limit = limit
        self._Acquisition__known_good = []

    @classmethod
    def fromJSON--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'json_path'
                4  LOAD_STR                 'r'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           86  'to 86'
               10  STORE_FAST               'handle'

 L.  53        12  LOAD_GLOBAL              json
               14  LOAD_METHOD              load
               16  LOAD_FAST                'handle'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'data'

 L.  55        22  BUILD_LIST_0          0 
               24  STORE_FAST               'packages'

 L.  56        26  LOAD_FAST                'data'
               28  GET_ITER         
               30  FOR_ITER             64  'to 64'
               32  STORE_FAST               'entry'

 L.  57        34  LOAD_GLOBAL              Package
               36  LOAD_FAST                'entry'
               38  LOAD_STR                 'name'
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'entry'
               44  LOAD_STR                 'files'
               46  BINARY_SUBSCR    
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'package'

 L.  58        52  LOAD_FAST                'packages'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'package'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  JUMP_BACK            30  'to 30'

 L.  60        64  LOAD_FAST                'cls'
               66  LOAD_FAST                'packages'
               68  LOAD_CONST               ('packages',)
               70  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               72  POP_BLOCK        
               74  ROT_TWO          
               76  BEGIN_FINALLY    
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  POP_FINALLY           0  ''
               84  RETURN_VALUE     
             86_0  COME_FROM_WITH        8  '8'
               86  WITH_CLEANUP_START
               88  WITH_CLEANUP_FINISH
               90  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 74

    def __load_knowngood(self):
        knowngood_path = os.path.join('data', 'knowngood.txt')
        knowngood_string = pkg_resources.resource_string(__name__, knowngood_path)
        knowngood_list = knowngood_string.decode'utf-8'.split'\n'
        self._Acquisition__known_good.extendknowngood_list

    def __clean_output(self, output):
        return output.strip().replace('package:', '')

    def connect--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              expanduser
                6  LOAD_STR                 '~/.android/adbkey'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'priv_key_path'

 L.  75        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'priv_key_path'
               16  LOAD_STR                 'rb'
               18  CALL_FUNCTION_2       2  ''
               20  SETUP_WITH           36  'to 36'
               22  STORE_FAST               'handle'

 L.  76        24  LOAD_FAST                'handle'
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'priv_key'
               32  POP_BLOCK        
               34  BEGIN_FINALLY    
             36_0  COME_FROM_WITH       20  '20'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

 L.  77        42  LOAD_FAST                'priv_key_path'
               44  LOAD_STR                 '.pub'
               46  BINARY_ADD       
               48  STORE_FAST               'pub_key_path'

 L.  78        50  LOAD_GLOBAL              open
               52  LOAD_FAST                'pub_key_path'
               54  LOAD_STR                 'rb'
               56  CALL_FUNCTION_2       2  ''
               58  SETUP_WITH           74  'to 74'
               60  STORE_FAST               'handle'

 L.  79        62  LOAD_FAST                'handle'
               64  LOAD_METHOD              read
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'pub_key'
               70  POP_BLOCK        
               72  BEGIN_FINALLY    
             74_0  COME_FROM_WITH       58  '58'
               74  WITH_CLEANUP_START
               76  WITH_CLEANUP_FINISH
               78  END_FINALLY      

 L.  81        80  LOAD_GLOBAL              sign_pythonrsa
               82  LOAD_METHOD              PythonRSASigner
               84  LOAD_FAST                'pub_key'
               86  LOAD_FAST                'priv_key'
               88  CALL_METHOD_2         2  ''
               90  STORE_FAST               'signer'

 L.  82        92  LOAD_GLOBAL              adb_commands
               94  LOAD_METHOD              AdbCommands
               96  CALL_METHOD_0         0  ''
               98  LOAD_FAST                'self'
              100  STORE_ATTR               device

 L.  85       102  SETUP_FINALLY       124  'to 124'

 L.  86       104  LOAD_FAST                'self'
              106  LOAD_ATTR                device
              108  LOAD_ATTR                ConnectDevice
              110  LOAD_FAST                'signer'
              112  BUILD_LIST_1          1 
              114  LOAD_CONST               ('rsa_keys',)
              116  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              118  POP_TOP          
              120  POP_BLOCK        
              122  BREAK_LOOP          276  'to 276'
            124_0  COME_FROM_FINALLY   102  '102'

 L.  87       124  DUP_TOP          
              126  LOAD_GLOBAL              USBErrorBusy
              128  LOAD_GLOBAL              USBErrorAccess
              130  BUILD_TUPLE_2         2 
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   168  'to 168'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L.  88       142  LOAD_GLOBAL              print
              144  LOAD_GLOBAL              error
              146  LOAD_STR                 'Device is busy, maybe run `adb kill-server` and try again.'
              148  CALL_FUNCTION_1       1  ''
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          

 L.  89       154  LOAD_GLOBAL              sys
              156  LOAD_METHOD              exit
              158  LOAD_CONST               -1
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  POP_EXCEPT       
              166  JUMP_BACK           102  'to 102'
            168_0  COME_FROM           134  '134'

 L.  90       168  DUP_TOP          
              170  LOAD_GLOBAL              DeviceAuthError
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   208  'to 208'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L.  91       182  LOAD_GLOBAL              print
              184  LOAD_GLOBAL              error
              186  LOAD_STR                 'You need to authorize this computer on the Android device. Retrying in 5 seconds...'
              188  CALL_FUNCTION_1       1  ''
              190  CALL_FUNCTION_1       1  ''
              192  POP_TOP          

 L.  92       194  LOAD_GLOBAL              time
              196  LOAD_METHOD              sleep
              198  LOAD_CONST               5
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          
              204  POP_EXCEPT       
              206  JUMP_BACK           102  'to 102'
            208_0  COME_FROM           174  '174'

 L.  93       208  DUP_TOP          
              210  LOAD_GLOBAL              Exception
              212  COMPARE_OP               exception-match
          214_216  POP_JUMP_IF_FALSE   268  'to 268'
              218  POP_TOP          
              220  STORE_FAST               'e'
              222  POP_TOP          
              224  SETUP_FINALLY       256  'to 256'

 L.  94       226  LOAD_GLOBAL              print
              228  LOAD_GLOBAL              error
              230  LOAD_GLOBAL              repr
              232  LOAD_FAST                'e'
              234  CALL_FUNCTION_1       1  ''
              236  CALL_FUNCTION_1       1  ''
              238  CALL_FUNCTION_1       1  ''
              240  POP_TOP          

 L.  95       242  LOAD_GLOBAL              sys
              244  LOAD_METHOD              exit
              246  LOAD_CONST               -1
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
              252  POP_BLOCK        
              254  BEGIN_FINALLY    
            256_0  COME_FROM_FINALLY   224  '224'
              256  LOAD_CONST               None
              258  STORE_FAST               'e'
              260  DELETE_FAST              'e'
              262  END_FINALLY      
              264  POP_EXCEPT       
              266  JUMP_BACK           102  'to 102'
            268_0  COME_FROM           214  '214'
              268  END_FINALLY      

 L.  97   270_272  BREAK_LOOP          276  'to 276'
              274  JUMP_BACK           102  'to 102'

Parse error at or near `POP_TOP' instruction at offset 138

    def disconnect(self):
        self.device.Close()

    def reconnect(self):
        print(info('Reconnecting ...'))
        self.disconnect()
        self.connect()

    def get_packages(self):
        print(info('Retrieving package names ...'))
        if not self.all_apks:
            self._Acquisition__load_knowngood()
        output = self.device.Shell'pm list packages'
        total = 0
        for line in output.split'\n':
            package_name = self._Acquisition__clean_outputline
            if package_name == '':
                pass
            else:
                total += 1
                if (self.all_apks or package_name) in self._Acquisition__known_good:
                    pass
                else:
                    if package_name not in self.packages:
                        self.packages.appendPackage(package_name)
                    print(info('There are {} packages installed on the device. I selected {} for inspection.'.format(total, len(self.packages))))
                    print('')

    def pull_packages--- This code section failed: ---

 L. 133         0  LOAD_GLOBAL              print
                2  LOAD_GLOBAL              info
                4  LOAD_STR                 'Starting acquisition at folder {}\n'
                6  LOAD_METHOD              format
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                storage_folder
               12  CALL_METHOD_1         1  ''
               14  CALL_FUNCTION_1       1  ''
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L. 135        20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              exists
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                storage_folder
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     46  'to 46'

 L. 136        34  LOAD_GLOBAL              os
               36  LOAD_METHOD              mkdir
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                storage_folder
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
             46_0  COME_FROM            32  '32'

 L. 138        46  LOAD_GLOBAL              print
               48  LOAD_GLOBAL              info
               50  LOAD_STR                 'Downloading packages from device. This might take some time ...'
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  POP_TOP          

 L. 139        58  LOAD_GLOBAL              print
               60  LOAD_STR                 ''
               62  CALL_FUNCTION_1       1  ''
               64  POP_TOP          

 L. 141        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              join
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                storage_folder
               76  LOAD_STR                 'apks'
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'storage_folder_apk'

 L. 142        82  LOAD_GLOBAL              os
               84  LOAD_ATTR                path
               86  LOAD_METHOD              exists
               88  LOAD_FAST                'storage_folder_apk'
               90  CALL_METHOD_1         1  ''
               92  POP_JUMP_IF_TRUE    104  'to 104'

 L. 143        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              mkdir
               98  LOAD_FAST                'storage_folder_apk'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
            104_0  COME_FROM            92  '92'

 L. 145       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                packages
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'total_packages'

 L. 146       114  LOAD_CONST               0
              116  STORE_FAST               'counter'

 L. 147       118  LOAD_FAST                'self'
              120  LOAD_ATTR                packages
              122  GET_ITER         
          124_126  FOR_ITER            656  'to 656'
              128  STORE_FAST               'package'

 L. 149       130  LOAD_FAST                'self'
              132  LOAD_ATTR                limit
              134  POP_JUMP_IF_FALSE   156  'to 156'
              136  LOAD_FAST                'counter'
              138  LOAD_GLOBAL              int
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                limit
              144  CALL_FUNCTION_1       1  ''
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   156  'to 156'

 L. 150       150  POP_TOP          
          152_154  JUMP_ABSOLUTE       656  'to 656'
            156_0  COME_FROM           148  '148'
            156_1  COME_FROM           134  '134'

 L. 152       156  LOAD_FAST                'counter'
              158  LOAD_CONST               1
              160  INPLACE_ADD      
              162  STORE_FAST               'counter'

 L. 154       164  LOAD_GLOBAL              print
              166  LOAD_STR                 '[{}/{}] Package: {}'
              168  LOAD_METHOD              format
              170  LOAD_FAST                'counter'
              172  LOAD_FAST                'total_packages'
              174  LOAD_GLOBAL              highlight
              176  LOAD_FAST                'package'
              178  LOAD_ATTR                name
              180  CALL_FUNCTION_1       1  ''
              182  CALL_METHOD_3         3  ''
              184  CALL_FUNCTION_1       1  ''
              186  POP_TOP          

 L. 156       188  SETUP_FINALLY       232  'to 232'

 L. 157       190  LOAD_FAST                'self'
              192  LOAD_ATTR                device
              194  LOAD_METHOD              Shell
              196  LOAD_STR                 'pm path {}'
              198  LOAD_METHOD              format
              200  LOAD_FAST                'package'
              202  LOAD_ATTR                name
              204  CALL_METHOD_1         1  ''
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'output'

 L. 158       210  LOAD_FAST                'self'
              212  LOAD_METHOD              _Acquisition__clean_output
              214  LOAD_FAST                'output'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'output'

 L. 159       220  LOAD_FAST                'output'
              222  POP_JUMP_IF_TRUE    228  'to 228'

 L. 160       224  POP_BLOCK        
              226  JUMP_BACK           124  'to 124'
            228_0  COME_FROM           222  '222'
              228  POP_BLOCK        
              230  JUMP_FORWARD        302  'to 302'
            232_0  COME_FROM_FINALLY   188  '188'

 L. 161       232  DUP_TOP          
              234  LOAD_GLOBAL              Exception
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   300  'to 300'
              242  POP_TOP          
              244  STORE_FAST               'e'
              246  POP_TOP          
              248  SETUP_FINALLY       288  'to 288'

 L. 162       250  LOAD_GLOBAL              print
              252  LOAD_STR                 'ERROR: Failed to get path of package {}: {}'
              254  LOAD_METHOD              format
              256  LOAD_FAST                'package'
              258  LOAD_ATTR                name
              260  LOAD_FAST                'e'
              262  CALL_METHOD_2         2  ''
              264  CALL_FUNCTION_1       1  ''
              266  POP_TOP          

 L. 163       268  LOAD_FAST                'self'
              270  LOAD_METHOD              reconnect
              272  CALL_METHOD_0         0  ''
              274  POP_TOP          

 L. 164       276  POP_BLOCK        
              278  POP_EXCEPT       
              280  CALL_FINALLY        288  'to 288'
              282  JUMP_BACK           124  'to 124'
              284  POP_BLOCK        
              286  BEGIN_FINALLY    
            288_0  COME_FROM           280  '280'
            288_1  COME_FROM_FINALLY   248  '248'
              288  LOAD_CONST               None
              290  STORE_FAST               'e'
              292  DELETE_FAST              'e'
              294  END_FINALLY      
              296  POP_EXCEPT       
              298  JUMP_FORWARD        302  'to 302'
            300_0  COME_FROM           238  '238'
              300  END_FINALLY      
            302_0  COME_FROM           298  '298'
            302_1  COME_FROM           230  '230'

 L. 168       302  LOAD_FAST                'output'
              304  LOAD_METHOD              split
              306  LOAD_STR                 '\n'
              308  CALL_METHOD_1         1  ''
              310  GET_ITER         
          312_314  FOR_ITER            646  'to 646'
              316  STORE_FAST               'path'

 L. 169       318  LOAD_FAST                'path'
              320  LOAD_METHOD              strip
              322  CALL_METHOD_0         0  ''
              324  STORE_FAST               'path'

 L. 170       326  LOAD_GLOBAL              print
              328  LOAD_STR                 'Downloading {} ...'
              330  LOAD_METHOD              format
              332  LOAD_FAST                'path'
              334  CALL_METHOD_1         1  ''
              336  CALL_FUNCTION_1       1  ''
              338  POP_TOP          

 L. 172       340  SETUP_FINALLY       392  'to 392'

 L. 173       342  LOAD_GLOBAL              PullProgress
              344  LOAD_STR                 'B'
              346  LOAD_CONST               1024
              348  LOAD_CONST               True
              350  LOAD_CONST               1
              352  LOAD_CONST               ('unit', 'unit_divisor', 'unit_scale', 'miniters')
              354  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              356  SETUP_WITH          382  'to 382'
              358  STORE_FAST               'pp'

 L. 174       360  LOAD_FAST                'self'
              362  LOAD_ATTR                device
              364  LOAD_ATTR                Pull
              366  LOAD_FAST                'path'
              368  LOAD_FAST                'pp'
              370  LOAD_ATTR                update_to
              372  LOAD_CONST               ('progress_callback',)
              374  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              376  STORE_FAST               'data'
              378  POP_BLOCK        
              380  BEGIN_FINALLY    
            382_0  COME_FROM_WITH      356  '356'
              382  WITH_CLEANUP_START
              384  WITH_CLEANUP_FINISH
              386  END_FINALLY      
              388  POP_BLOCK        
              390  JUMP_FORWARD        462  'to 462'
            392_0  COME_FROM_FINALLY   340  '340'

 L. 175       392  DUP_TOP          
              394  LOAD_GLOBAL              Exception
              396  COMPARE_OP               exception-match
          398_400  POP_JUMP_IF_FALSE   460  'to 460'
              402  POP_TOP          
              404  STORE_FAST               'e'
              406  POP_TOP          
              408  SETUP_FINALLY       448  'to 448'

 L. 176       410  LOAD_GLOBAL              print
              412  LOAD_STR                 'ERROR: Failed to pull package file from {}: {}'
              414  LOAD_METHOD              format
              416  LOAD_FAST                'path'
              418  LOAD_FAST                'e'
              420  CALL_METHOD_2         2  ''
              422  CALL_FUNCTION_1       1  ''
              424  POP_TOP          

 L. 177       426  LOAD_FAST                'self'
              428  LOAD_METHOD              reconnect
              430  CALL_METHOD_0         0  ''
              432  POP_TOP          

 L. 178       434  POP_BLOCK        
              436  POP_EXCEPT       
              438  CALL_FINALLY        448  'to 448'
          440_442  JUMP_BACK           312  'to 312'
              444  POP_BLOCK        
              446  BEGIN_FINALLY    
            448_0  COME_FROM           438  '438'
            448_1  COME_FROM_FINALLY   408  '408'
              448  LOAD_CONST               None
              450  STORE_FAST               'e'
              452  DELETE_FAST              'e'
              454  END_FINALLY      
              456  POP_EXCEPT       
              458  JUMP_FORWARD        462  'to 462'
            460_0  COME_FROM           398  '398'
              460  END_FINALLY      
            462_0  COME_FROM           458  '458'
            462_1  COME_FROM           390  '390'

 L. 181       462  LOAD_STR                 ''
              464  STORE_FAST               'file_name'

 L. 182       466  LOAD_STR                 '==/'
              468  LOAD_FAST                'path'
              470  COMPARE_OP               in
          472_474  POP_JUMP_IF_FALSE   502  'to 502'

 L. 183       476  LOAD_STR                 '_'
              478  LOAD_FAST                'path'
              480  LOAD_METHOD              split
              482  LOAD_STR                 '==/'
              484  CALL_METHOD_1         1  ''
              486  LOAD_CONST               1
              488  BINARY_SUBSCR    
              490  LOAD_METHOD              replace
              492  LOAD_STR                 '.apk'
              494  LOAD_STR                 ''
              496  CALL_METHOD_2         2  ''
              498  BINARY_ADD       
              500  STORE_FAST               'file_name'
            502_0  COME_FROM           472  '472'

 L. 186       502  LOAD_GLOBAL              os
              504  LOAD_ATTR                path
              506  LOAD_METHOD              join
              508  LOAD_FAST                'storage_folder_apk'
              510  LOAD_STR                 '{}{}.apk'
              512  LOAD_METHOD              format
              514  LOAD_FAST                'package'
              516  LOAD_ATTR                name
              518  LOAD_FAST                'file_name'
              520  CALL_METHOD_2         2  ''
              522  CALL_METHOD_2         2  ''
              524  STORE_FAST               'file_path'

 L. 187       526  LOAD_CONST               0
              528  STORE_FAST               'name_counter'

 L. 189       530  LOAD_GLOBAL              os
              532  LOAD_ATTR                path
              534  LOAD_METHOD              exists
              536  LOAD_FAST                'file_path'
              538  CALL_METHOD_1         1  ''
          540_542  POP_JUMP_IF_TRUE    548  'to 548'

 L. 190   544_546  BREAK_LOOP          586  'to 586'
            548_0  COME_FROM           540  '540'

 L. 192       548  LOAD_FAST                'name_counter'
              550  LOAD_CONST               1
              552  INPLACE_ADD      
              554  STORE_FAST               'name_counter'

 L. 193       556  LOAD_GLOBAL              os
              558  LOAD_ATTR                path
              560  LOAD_METHOD              join
              562  LOAD_FAST                'storage_folder_apk'
              564  LOAD_STR                 '{}{}_{}.apk'
              566  LOAD_METHOD              format

 L. 194       568  LOAD_FAST                'package'
              570  LOAD_ATTR                name

 L. 194       572  LOAD_FAST                'file_name'

 L. 194       574  LOAD_FAST                'name_counter'

 L. 193       576  CALL_METHOD_3         3  ''
              578  CALL_METHOD_2         2  ''
              580  STORE_FAST               'file_path'
          582_584  JUMP_BACK           530  'to 530'

 L. 196       586  LOAD_GLOBAL              open
              588  LOAD_FAST                'file_path'
              590  LOAD_STR                 'wb'
              592  CALL_FUNCTION_2       2  ''
              594  SETUP_WITH          612  'to 612'
              596  STORE_FAST               'handle'

 L. 197       598  LOAD_FAST                'handle'
              600  LOAD_METHOD              write
              602  LOAD_FAST                'data'
              604  CALL_METHOD_1         1  ''
              606  POP_TOP          
              608  POP_BLOCK        
              610  BEGIN_FINALLY    
            612_0  COME_FROM_WITH      594  '594'
              612  WITH_CLEANUP_START
              614  WITH_CLEANUP_FINISH
              616  END_FINALLY      

 L. 200       618  LOAD_FAST                'package'
              620  LOAD_ATTR                files
              622  LOAD_METHOD              append

 L. 201       624  LOAD_FAST                'path'

 L. 202       626  LOAD_FAST                'file_path'

 L. 203       628  LOAD_GLOBAL              get_sha256
              630  LOAD_FAST                'file_path'
              632  CALL_FUNCTION_1       1  ''

 L. 200       634  LOAD_CONST               ('path', 'stored_path', 'sha256')
              636  BUILD_CONST_KEY_MAP_3     3 
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          
          642_644  JUMP_BACK           312  'to 312'

 L. 206       646  LOAD_GLOBAL              print
              648  LOAD_STR                 ''
              650  CALL_FUNCTION_1       1  ''
              652  POP_TOP          
              654  JUMP_BACK           124  'to 124'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 152_154

    def save_json(self):
        json_path = os.path.join(self.storage_folder, 'packages.json')
        packages = []
        for package in self.packages:
            packages.appendpackage.__dict__
        else:
            with openjson_path'w' as (handle):
                json.dump(packages, handle, indent=4)

    def run(self):
        self.connect()
        self.get_packages()
        self.pull_packages()
        self.disconnect()
        self.save_json()