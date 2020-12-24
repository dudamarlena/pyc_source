# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mdt/command.py
# Compiled at: 2019-09-10 14:32:03
# Size of source mod 2**32: 4232 bytes
"""
Copyright 2019 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re, os, socket
from time import sleep
from paramiko.ssh_exception import SSHException
from mdt import config
from mdt import console
from mdt import discoverer
from mdt import sshclient
IP_ADDR_REGEX = re.compile('[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}')

class NetworkCommand:

    def __init__(self):
        self.config = config.Config()
        self.discoverer = discoverer.Discoverer(self)
        self.device = self.config.preferredDevice()
        self.address = None

    def add_device(self, hostname, address):
        if not self.device:
            self.device = hostname
            self.address = address
        elif self.device == hostname:
            self.address = address

    def run--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  LOAD_ATTR                preConnectRun
                4  LOAD_FAST                'args'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  POP_JUMP_IF_TRUE     14  'to 14'

 L.  51        10  LOAD_CONST               1
               12  RETURN_END_IF    
             14_0  COME_FROM             8  '8'

 L.  55        14  LOAD_FAST                'self'
               16  LOAD_ATTR                device
               18  POP_JUMP_IF_FALSE    40  'to 40'
               20  LOAD_GLOBAL              IP_ADDR_REGEX
               22  LOAD_ATTR                match
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                device
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L.  56        32  LOAD_FAST                'self'
               34  LOAD_ATTR                device
               36  LOAD_FAST                'self'
               38  STORE_ATTR               address
             40_0  COME_FROM            30  '30'
             40_1  COME_FROM            18  '18'

 L.  58        40  LOAD_FAST                'self'
               42  LOAD_ATTR                address
               44  POP_JUMP_IF_TRUE     88  'to 88'

 L.  59        46  LOAD_FAST                'self'
               48  LOAD_ATTR                device
               50  POP_JUMP_IF_FALSE    70  'to 70'

 L.  60        52  LOAD_GLOBAL              print
               54  LOAD_STR                 'Waiting for device {0}...'
               56  LOAD_ATTR                format
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                device
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  POP_TOP          
               68  JUMP_FORWARD         78  'to 78'
               70  ELSE                     '78'

 L.  62        70  LOAD_GLOBAL              print
               72  LOAD_STR                 'Waiting for a device...'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          
             78_0  COME_FROM            68  '68'

 L.  63        78  LOAD_FAST                'self'
               80  LOAD_ATTR                discoverer
               82  LOAD_ATTR                discover
               84  CALL_FUNCTION_0       0  '0 positional arguments'
               86  POP_TOP          
             88_0  COME_FROM            44  '44'

 L.  65        88  LOAD_FAST                'self'
               90  LOAD_ATTR                address
               92  POP_JUMP_IF_TRUE    130  'to 130'

 L.  66        94  LOAD_FAST                'self'
               96  LOAD_ATTR                device
               98  POP_JUMP_IF_TRUE    110  'to 110'

 L.  67       100  LOAD_GLOBAL              print
              102  LOAD_STR                 'Unable to find any devices on your local network segment.'
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  POP_TOP          
              108  JUMP_FORWARD        126  'to 126'
              110  ELSE                     '126'

 L.  69       110  LOAD_GLOBAL              print
              112  LOAD_STR                 'Unable to find a device called {0} on your local network segment.'
              114  LOAD_ATTR                format
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                device
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  POP_TOP          
            126_0  COME_FROM           108  '108'

 L.  70       126  LOAD_CONST               1
              128  RETURN_END_IF    
            130_0  COME_FROM            92  '92'

 L.  72       130  LOAD_CONST               None
              132  STORE_FAST               'client'

 L.  73       134  SETUP_FINALLY       596  'to 596'
              138  SETUP_EXCEPT        188  'to 188'

 L.  74       140  LOAD_GLOBAL              print
              142  LOAD_STR                 'Connecting to {0} at {1}'
              144  LOAD_ATTR                format
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                device
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                address
              154  CALL_FUNCTION_2       2  '2 positional arguments'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  POP_TOP          

 L.  75       160  LOAD_GLOBAL              sshclient
              162  LOAD_ATTR                SshClient
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                device
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                address
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  STORE_FAST               'client'

 L.  76       176  LOAD_FAST                'self'
              178  LOAD_ATTR                runWithClient
              180  LOAD_FAST                'client'
              182  LOAD_FAST                'args'
              184  CALL_FUNCTION_2       2  '2 positional arguments'
              186  RETURN_VALUE     
            188_0  COME_FROM_EXCEPT    138  '138'

 L.  77       188  DUP_TOP          
              190  LOAD_GLOBAL              sshclient
              192  LOAD_ATTR                KeyPushError
              194  COMPARE_OP               exception-match
              196  POP_JUMP_IF_FALSE   238  'to 238'
              200  POP_TOP          
              202  STORE_FAST               'e'
              204  POP_TOP          
              206  SETUP_FINALLY       226  'to 226'

 L.  78       208  LOAD_GLOBAL              print
              210  LOAD_STR                 'Unable to push keys to the device: {0}'
              212  LOAD_ATTR                format
              214  LOAD_FAST                'e'
              216  CALL_FUNCTION_1       1  '1 positional argument'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  POP_TOP          

 L.  79       222  LOAD_CONST               1
              224  RETURN_VALUE     
            226_0  COME_FROM_FINALLY   206  '206'
              226  LOAD_CONST               None
              228  STORE_FAST               'e'
              230  DELETE_FAST              'e'
              232  END_FINALLY      
              234  JUMP_FORWARD        592  'to 592'

 L.  80       238  DUP_TOP          
              240  LOAD_GLOBAL              sshclient
              242  LOAD_ATTR                DefaultLoginError
              244  COMPARE_OP               exception-match
              246  POP_JUMP_IF_FALSE   288  'to 288'
              250  POP_TOP          
              252  STORE_FAST               'e'
              254  POP_TOP          
              256  SETUP_FINALLY       276  'to 276'

 L.  81       258  LOAD_GLOBAL              print
              260  LOAD_STR                 "Can't login using default credentials: {0}"
              262  LOAD_ATTR                format
              264  LOAD_FAST                'e'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  POP_TOP          

 L.  82       272  LOAD_CONST               1
              274  RETURN_VALUE     
            276_0  COME_FROM_FINALLY   256  '256'
              276  LOAD_CONST               None
              278  STORE_FAST               'e'
              280  DELETE_FAST              'e'
              282  END_FINALLY      
              284  JUMP_FORWARD        592  'to 592'

 L.  83       288  DUP_TOP          
              290  LOAD_GLOBAL              sshclient
              292  LOAD_ATTR                NonLocalDeviceError
              294  COMPARE_OP               exception-match
              296  POP_JUMP_IF_FALSE   352  'to 352'
              300  POP_TOP          
              302  STORE_FAST               'e'
              304  POP_TOP          
              306  SETUP_FINALLY       340  'to 340'

 L.  84       308  LOAD_GLOBAL              print
              310  CALL_FUNCTION_0       0  '0 positional arguments'
              312  POP_TOP          

 L.  85       314  LOAD_GLOBAL              print
              316  LOAD_STR                 "It looks like you're trying to connect to a device that isn't connected\nto your workstation via USB and doesn't have the SSH key this MDT generated.\nTo connect with `mdt shell` you will need to first connect to your device\nONLY via USB."
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  POP_TOP          

 L.  89       322  LOAD_GLOBAL              print
              324  CALL_FUNCTION_0       0  '0 positional arguments'
              326  POP_TOP          

 L.  90       328  LOAD_GLOBAL              print
              330  LOAD_STR                 'Cowardly refusing to attempt to push a key to a public machine.\n'
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  POP_TOP          

 L.  91       336  LOAD_CONST               1
              338  RETURN_VALUE     
            340_0  COME_FROM_FINALLY   306  '306'
              340  LOAD_CONST               None
              342  STORE_FAST               'e'
              344  DELETE_FAST              'e'
              346  END_FINALLY      
              348  JUMP_FORWARD        592  'to 592'
              352  ELSE                     '592'

 L.  92       352  DUP_TOP          
              354  LOAD_GLOBAL              SSHException
              356  COMPARE_OP               exception-match
              358  POP_JUMP_IF_FALSE   398  'to 398'
              362  POP_TOP          
              364  STORE_FAST               'e'
              366  POP_TOP          
              368  SETUP_FINALLY       388  'to 388'

 L.  93       370  LOAD_GLOBAL              print
              372  LOAD_STR                 "Couldn't establish ssh connection to device: {0}"
              374  LOAD_ATTR                format
              376  LOAD_FAST                'e'
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  POP_TOP          

 L.  94       384  LOAD_CONST               1
              386  RETURN_VALUE     
            388_0  COME_FROM_FINALLY   368  '368'
              388  LOAD_CONST               None
              390  STORE_FAST               'e'
              392  DELETE_FAST              'e'
              394  END_FINALLY      
              396  JUMP_FORWARD        592  'to 592'

 L.  95       398  DUP_TOP          
              400  LOAD_GLOBAL              socket
              402  LOAD_ATTR                error
              404  COMPARE_OP               exception-match
              406  POP_JUMP_IF_FALSE   446  'to 446'
              410  POP_TOP          
              412  STORE_FAST               'e'
              414  POP_TOP          
              416  SETUP_FINALLY       436  'to 436'

 L.  96       418  LOAD_GLOBAL              print
              420  LOAD_STR                 "Couldn't establish ssh connection to device: socket error: {0}"
              422  LOAD_ATTR                format

 L.  97       424  LOAD_FAST                'e'
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  POP_TOP          

 L.  98       432  LOAD_CONST               1
              434  RETURN_VALUE     
            436_0  COME_FROM_FINALLY   416  '416'
              436  LOAD_CONST               None
              438  STORE_FAST               'e'
              440  DELETE_FAST              'e'
              442  END_FINALLY      
              444  JUMP_FORWARD        592  'to 592'

 L.  99       446  DUP_TOP          
              448  LOAD_GLOBAL              console
              450  LOAD_ATTR                SocketTimeoutError
              452  COMPARE_OP               exception-match
              454  POP_JUMP_IF_FALSE   500  'to 500'
              458  POP_TOP          
              460  STORE_FAST               'e'
              462  POP_TOP          
              464  SETUP_FINALLY       490  'to 490'

 L. 100       466  LOAD_GLOBAL              print
              468  LOAD_STR                 '\r\nConnection to {0} at {1} closed: socket timeout'
              470  LOAD_ATTR                format

 L. 101       472  LOAD_FAST                'self'
              474  LOAD_ATTR                device
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                address
              480  CALL_FUNCTION_2       2  '2 positional arguments'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  POP_TOP          

 L. 102       486  LOAD_CONST               1
              488  RETURN_VALUE     
            490_0  COME_FROM_FINALLY   464  '464'
              490  LOAD_CONST               None
              492  STORE_FAST               'e'
              494  DELETE_FAST              'e'
              496  END_FINALLY      
              498  JUMP_FORWARD        592  'to 592'

 L. 103       500  DUP_TOP          
              502  LOAD_GLOBAL              console
              504  LOAD_ATTR                ConnectionClosedError
              506  COMPARE_OP               exception-match
              508  POP_JUMP_IF_FALSE   590  'to 590'
              512  POP_TOP          
              514  STORE_FAST               'e'
              516  POP_TOP          
              518  SETUP_FINALLY       580  'to 580'

 L. 104       520  LOAD_FAST                'e'
              522  LOAD_ATTR                exit_code
              524  POP_JUMP_IF_FALSE   554  'to 554'

 L. 105       528  LOAD_GLOBAL              print
              530  LOAD_STR                 '\r\nConnection to {0} at {1} closed with exit code {2}'
              532  LOAD_ATTR                format

 L. 106       534  LOAD_FAST                'self'
              536  LOAD_ATTR                device
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                address
              542  LOAD_FAST                'e'
              544  LOAD_ATTR                exit_code
              546  CALL_FUNCTION_3       3  '3 positional arguments'
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  POP_TOP          
              552  JUMP_FORWARD        574  'to 574'
              554  ELSE                     '574'

 L. 108       554  LOAD_GLOBAL              print
              556  LOAD_STR                 '\r\nConnection to {0} at {1} closed'
              558  LOAD_ATTR                format

 L. 109       560  LOAD_FAST                'self'
              562  LOAD_ATTR                device
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                address
              568  CALL_FUNCTION_2       2  '2 positional arguments'
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  POP_TOP          
            574_0  COME_FROM           552  '552'

 L. 110       574  LOAD_FAST                'e'
              576  LOAD_ATTR                exit_code
              578  RETURN_VALUE     
            580_0  COME_FROM_FINALLY   518  '518'
              580  LOAD_CONST               None
              582  STORE_FAST               'e'
              584  DELETE_FAST              'e'
              586  END_FINALLY      
              588  JUMP_FORWARD        592  'to 592'
              590  END_FINALLY      
            592_0  COME_FROM           588  '588'
            592_1  COME_FROM           498  '498'
            592_2  COME_FROM           444  '444'
            592_3  COME_FROM           396  '396'
            592_4  COME_FROM           348  '348'
            592_5  COME_FROM           284  '284'
            592_6  COME_FROM           234  '234'
              592  POP_BLOCK        
              594  LOAD_CONST               None
            596_0  COME_FROM_FINALLY   134  '134'

 L. 112       596  LOAD_FAST                'client'
              598  POP_JUMP_IF_FALSE   610  'to 610'

 L. 113       602  LOAD_FAST                'client'
              604  LOAD_ATTR                close
              606  CALL_FUNCTION_0       0  '0 positional arguments'
              608  POP_TOP          
            610_0  COME_FROM           598  '598'
              610  END_FINALLY      

Parse error at or near `ELSE' instruction at offset 352

    def runWithClient(self, client, args):
        return 1

    def preConnectRun(self, args):
        return True