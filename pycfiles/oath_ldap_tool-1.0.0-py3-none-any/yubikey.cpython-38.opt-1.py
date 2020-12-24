# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oathldap_tool/yubikey.py
# Compiled at: 2020-03-29 20:40:47
# Size of source mod 2**32: 7723 bytes
"""
oathldap_tool.yubikey -- low-level Yubikey stuff
"""
import time
from binascii import unhexlify
import yubico.yubikey_defs
from yubico.yubikey_base import YubiKeyError
from yubico import find_yubikey
from yubico.yubikey_config import YubiKeyConfig
from yubico.yubikey_neo_usb_hid import YubiKeyNEO_NDEF, YubiKeyNEO_DEVICE_CONFIG
__all__ = [
 'YK_SCAN_CODE',
 'YK_PASSWORD_ALPHABET',
 'YubiKeySearchError',
 'YKTokenDevice']
YK_SCAN_CODE = 'h:9284978b2c869291898c8a2c9a849691972c868f88849588871b2c87922c8c972c848a848c91'
YK_PASSWORD_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'

class YubiKeySearchError(Exception):
    __doc__ = '\n    to be raised if search for a single Yubikey device failed\n    '


class YKTokenDevice:
    __doc__ = '\n    a single slot of a Yubikey token\n    '
    find_yubikey_max_skip = 6

    def __init__(self, key):
        self.key = key

    @classmethod
    def search--- This code section failed: ---

 L.  49         0  BUILD_LIST_0          0 
                2  STORE_FAST               'yk_devices'

 L.  50         4  LOAD_CONST               0
                6  STORE_FAST               'skip'

 L.  52         8  SETUP_FINALLY        24  'to 24'

 L.  53        10  LOAD_GLOBAL              find_yubikey
               12  LOAD_FAST                'skip'
               14  LOAD_CONST               ('skip',)
               16  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               18  STORE_FAST               'yk_dev'
               20  POP_BLOCK        
               22  JUMP_FORWARD         90  'to 90'
             24_0  COME_FROM_FINALLY     8  '8'

 L.  54        24  DUP_TOP          
               26  LOAD_GLOBAL              YubiKeyError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    88  'to 88'
               32  POP_TOP          
               34  STORE_FAST               'yk_error'
               36  POP_TOP          
               38  SETUP_FINALLY        76  'to 76'

 L.  55        40  LOAD_FAST                'yk_error'
               42  LOAD_ATTR                reason
               44  LOAD_STR                 'No YubiKey found'
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L.  56        50  LOAD_FAST                'yk_error'
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            48  '48'

 L.  58        54  LOAD_FAST                'skip'
               56  LOAD_FAST                'cls'
               58  LOAD_ATTR                find_yubikey_max_skip
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L.  59        64  POP_BLOCK        
               66  POP_EXCEPT       
               68  CALL_FINALLY         76  'to 76'
               70  BREAK_LOOP          110  'to 110'
             72_0  COME_FROM            62  '62'
               72  POP_BLOCK        
               74  BEGIN_FINALLY    
             76_0  COME_FROM            68  '68'
             76_1  COME_FROM_FINALLY    38  '38'
               76  LOAD_CONST               None
               78  STORE_FAST               'yk_error'
               80  DELETE_FAST              'yk_error'
               82  END_FINALLY      
               84  POP_EXCEPT       
               86  JUMP_FORWARD        100  'to 100'
             88_0  COME_FROM            30  '30'
               88  END_FINALLY      
             90_0  COME_FROM            22  '22'

 L.  61        90  LOAD_FAST                'yk_devices'
               92  LOAD_METHOD              append
               94  LOAD_FAST                'yk_dev'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
            100_0  COME_FROM            86  '86'

 L.  62       100  LOAD_FAST                'skip'
              102  LOAD_CONST               1
              104  INPLACE_ADD      
              106  STORE_FAST               'skip'
              108  JUMP_BACK             8  'to 8'

 L.  63       110  LOAD_FAST                'yk_devices'
              112  POP_JUMP_IF_TRUE    122  'to 122'

 L.  64       114  LOAD_GLOBAL              YubiKeySearchError
              116  LOAD_STR                 'No Yubikey devices found!'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L.  65       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'yk_devices'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_CONST               1
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L.  66       134  LOAD_GLOBAL              YubiKeySearchError
              136  LOAD_STR                 'More than one Yubikey found. Only one allowed!'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           132  '132'

 L.  67       142  LOAD_FAST                'cls'
              144  LOAD_FAST                'yk_devices'
              146  LOAD_CONST               0
              148  BINARY_SUBSCR    
              150  CALL_FUNCTION_1       1  ''
              152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 66

    def info(self):
        """
        return dict with various device information
        """
        return dict(model=(self.key.model),
          serial=(self.key.serial()),
          version=(self.key.version()),
          status=(self.key.status()))

    def info_msg(self):
        """
        returns string with info about the device
        """
        info = self.info()
        info.update(slots=(', '.joinmap(str, info['status'].valid_configs()) or 'none'))
        return ('{model} no. {serial} {version} // Enabled slots: {slots}'.format)(**info)

    def enabled_slots(self):
        """
        returns list of numbers of enabled/configured slots
        """
        return self.key.status().valid_configs()

    def _write_cfg(self, ykcfg, slot):
        """
        write Yubikey configuration given in :cfg: to :slot:
        """
        if isinstance(ykcfg, YubiKeyConfig):
            self.key.write_config(ykcfg, slot)
        else:
            if isinstance(ykcfg, YubiKeyNEO_NDEF):
                self.key.write_ndef(ykcfg, slot)
            else:
                if isinstance(ykcfg, YubiKeyNEO_DEVICE_CONFIG):
                    self.key.write_device_configykcfg
                else:
                    raise Exception('Wrong config type: %s' % repr(ykcfg))

    def init_hotp(self, slot, oath_secret, otp_len, oath_tokenid, access_code):
        """
        Initialize a device slot for HOTP
        """
        self.set_mode(slot, yubico.yubikey_defs.MODE.OTP)
        cfg = self.key.init_config()
        if oath_tokenid:
            if not oath_tokenid.startswith'ubhe':
                raise ValueError('Expected oath_tokenid with prefix "ubhe", but was %r' % oath_tokenid)
            cfg.mode_oath_hotp(secret=oath_secret,
              digits=otp_len,
              omp=225,
              tt=99,
              mui=(b'h:' + oath_tokenid[4:].encode'ascii'))
            cfg.config_flag('OATH_FIXED_MODHEX2', True)
        else:
            cfg.mode_oath_hotp(secret=oath_secret, digits=otp_len)
        cfg.access_keyaccess_code.encode'ascii'
        cfg.ticket_flag('APPEND_CR', False)
        cfg.ticket_flag('PROTECT_CFG2', True)
        cfg.extended_flag('SERIAL_API_VISIBLE', True)
        cfg.extended_flag('ALLOW_UPDATE', False)
        cfg.extended_flag('FAST_TRIG', True)
        self._write_cfg(cfg, slot)

    def is_enabled(self, slot):
        """
        check wether slot is already enabled/configured
        """
        return slot in self.key.status().valid_configs()

    def _write_scancode--- This code section failed: ---

 L. 156         0  LOAD_FAST                'scancode'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 'h:'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    46  'to 46'
               10  LOAD_FAST                'scancode'
               12  LOAD_STR                 'h:'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_TRUE     46  'to 46'

 L. 157        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'scancode'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               78
               26  COMPARE_OP               >

 L. 156        28  POP_JUMP_IF_TRUE     46  'to 46'

 L. 157        30  LOAD_GLOBAL              len
               32  LOAD_FAST                'scancode'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_CONST               2
               38  BINARY_MODULO    
               40  LOAD_CONST               0
               42  COMPARE_OP               !=

 L. 156        44  POP_JUMP_IF_FALSE    62  'to 62'
             46_0  COME_FROM            28  '28'
             46_1  COME_FROM            16  '16'
             46_2  COME_FROM             8  '8'

 L. 158        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'Invalid scancode %s'
               50  LOAD_GLOBAL              repr
               52  LOAD_FAST                'scancode'
               54  CALL_FUNCTION_1       1  ''
               56  BINARY_MODULO    
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            44  '44'

 L. 159        62  LOAD_FAST                'scancode'
               64  LOAD_CONST               2
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  STORE_FAST               'scancode'

 L. 160        74  LOAD_FAST                'self'
               76  LOAD_ATTR                key
               78  LOAD_METHOD              init_config
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'cfg'

 L. 161        84  LOAD_FAST                'cfg'
               86  LOAD_METHOD              enable_extended_scan_code_mode
               88  CALL_METHOD_0         0  ''
               90  POP_TOP          

 L. 162        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'scancode'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_CONST               32
              100  COMPARE_OP               >
              102  POP_JUMP_IF_FALSE   144  'to 144'

 L. 163       104  LOAD_FAST                'scancode'
              106  LOAD_CONST               None
              108  LOAD_CONST               32
              110  BUILD_SLICE_2         2 
              112  BINARY_SUBSCR    
              114  STORE_FAST               'fixstr'

 L. 164       116  LOAD_FAST                'scancode'
              118  LOAD_CONST               32
              120  LOAD_CONST               None
              122  BUILD_SLICE_2         2 
              124  BINARY_SUBSCR    
              126  STORE_FAST               'scancode'

 L. 165       128  LOAD_FAST                'cfg'
              130  LOAD_METHOD              fixed_string
              132  LOAD_STR                 'h:'
              134  LOAD_FAST                'fixstr'
              136  BINARY_ADD       
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_FORWARD        178  'to 178'
            144_0  COME_FROM           102  '102'

 L. 166       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'scancode'
              148  CALL_FUNCTION_1       1  ''
              150  LOAD_CONST               1
              152  COMPARE_OP               >=
              154  POP_JUMP_IF_FALSE   178  'to 178'

 L. 167       156  LOAD_FAST                'scancode'
              158  STORE_FAST               'fixstr'

 L. 168       160  LOAD_STR                 ''
              162  STORE_FAST               'scancode'

 L. 169       164  LOAD_FAST                'cfg'
              166  LOAD_METHOD              fixed_string
              168  LOAD_STR                 'h:'
              170  LOAD_FAST                'fixstr'
              172  BINARY_ADD       
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          
            178_0  COME_FROM           154  '154'
            178_1  COME_FROM           142  '142'

 L. 170       178  LOAD_GLOBAL              len
              180  LOAD_FAST                'scancode'
              182  CALL_FUNCTION_1       1  ''
              184  LOAD_CONST               12
              186  COMPARE_OP               >
              188  POP_JUMP_IF_FALSE   226  'to 226'

 L. 171       190  LOAD_FAST                'scancode'
              192  LOAD_CONST               None
              194  LOAD_CONST               12
              196  BUILD_SLICE_2         2 
              198  BINARY_SUBSCR    
              200  STORE_FAST               'uidstr'

 L. 172       202  LOAD_FAST                'scancode'
              204  LOAD_CONST               12
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  STORE_FAST               'scancode'

 L. 173       214  LOAD_GLOBAL              unhexlify
              216  LOAD_FAST                'uidstr'
              218  CALL_FUNCTION_1       1  ''
              220  LOAD_FAST                'cfg'
              222  STORE_ATTR               uid
              224  JUMP_FORWARD        258  'to 258'
            226_0  COME_FROM           188  '188'

 L. 174       226  LOAD_GLOBAL              len
              228  LOAD_FAST                'scancode'
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_CONST               1
              234  COMPARE_OP               >=
          236_238  POP_JUMP_IF_FALSE   258  'to 258'

 L. 175       240  LOAD_FAST                'scancode'
              242  STORE_FAST               'uidstr'

 L. 176       244  LOAD_STR                 ''
              246  STORE_FAST               'scancode'

 L. 177       248  LOAD_GLOBAL              unhexlify
              250  LOAD_FAST                'uidstr'
              252  CALL_FUNCTION_1       1  ''
              254  LOAD_FAST                'cfg'
              256  STORE_ATTR               uid
            258_0  COME_FROM           236  '236'
            258_1  COME_FROM           224  '224'

 L. 178       258  LOAD_GLOBAL              len
              260  LOAD_FAST                'scancode'
              262  CALL_FUNCTION_1       1  ''
              264  LOAD_CONST               32
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   312  'to 312'

 L. 179       272  LOAD_FAST                'scancode'
              274  LOAD_CONST               None
              276  LOAD_CONST               32
              278  BUILD_SLICE_2         2 
              280  BINARY_SUBSCR    
              282  STORE_FAST               'aeskeystr'

 L. 180       284  LOAD_FAST                'scancode'
              286  LOAD_CONST               32
              288  LOAD_CONST               None
              290  BUILD_SLICE_2         2 
              292  BINARY_SUBSCR    
              294  STORE_FAST               'scancode'

 L. 181       296  LOAD_FAST                'cfg'
              298  LOAD_METHOD              aes_key
              300  LOAD_STR                 'h:'
              302  LOAD_FAST                'aeskeystr'
              304  BINARY_ADD       
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
              310  JUMP_FORWARD        356  'to 356'
            312_0  COME_FROM           268  '268'

 L. 182       312  LOAD_GLOBAL              len
              314  LOAD_FAST                'scancode'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_CONST               1
              320  COMPARE_OP               >=
          322_324  POP_JUMP_IF_FALSE   356  'to 356'

 L. 183       326  LOAD_FAST                'scancode'
              328  LOAD_METHOD              ljust
              330  LOAD_CONST               32
              332  LOAD_STR                 '0'
              334  CALL_METHOD_2         2  ''
              336  STORE_FAST               'aeskeystr'

 L. 184       338  LOAD_STR                 ''
              340  STORE_FAST               'scancode'

 L. 185       342  LOAD_FAST                'cfg'
              344  LOAD_METHOD              aes_key
              346  LOAD_STR                 'h:'
              348  LOAD_FAST                'aeskeystr'
              350  BINARY_ADD       
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
            356_0  COME_FROM           322  '322'
            356_1  COME_FROM           310  '310'

 L. 186       356  LOAD_FAST                'self'
              358  LOAD_METHOD              is_enabled
              360  LOAD_FAST                'slot'
              362  CALL_METHOD_1         1  ''
          364_366  POP_JUMP_IF_FALSE   390  'to 390'
              368  LOAD_FAST                'current_access_code'
          370_372  POP_JUMP_IF_FALSE   390  'to 390'

 L. 187       374  LOAD_FAST                'cfg'
              376  LOAD_METHOD              unlock_key
              378  LOAD_FAST                'current_access_code'
              380  LOAD_METHOD              encode
              382  LOAD_STR                 'ascii'
              384  CALL_METHOD_1         1  ''
              386  CALL_METHOD_1         1  ''
              388  POP_TOP          
            390_0  COME_FROM           370  '370'
            390_1  COME_FROM           364  '364'

 L. 188       390  LOAD_FAST                'cfg'
              392  LOAD_METHOD              extended_flag
              394  LOAD_STR                 'SERIAL_API_VISIBLE'
              396  LOAD_CONST               True
              398  CALL_METHOD_2         2  ''
              400  POP_TOP          

 L. 189       402  LOAD_FAST                'cfg'
              404  LOAD_METHOD              extended_flag
              406  LOAD_STR                 'ALLOW_UPDATE'
              408  LOAD_CONST               False
              410  CALL_METHOD_2         2  ''
              412  POP_TOP          

 L. 190       414  LOAD_FAST                'cfg'
              416  LOAD_METHOD              access_key
              418  LOAD_FAST                'access_code'
              420  LOAD_METHOD              encode
              422  LOAD_STR                 'ascii'
              424  CALL_METHOD_1         1  ''
              426  CALL_METHOD_1         1  ''
              428  POP_TOP          

 L. 191       430  LOAD_FAST                'self'
              432  LOAD_METHOD              _write_cfg
              434  LOAD_FAST                'cfg'
              436  LOAD_FAST                'slot'
              438  CALL_METHOD_2         2  ''
              440  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 438

    def reset_slot(self, slot, current_access_code):
        """
        reset the given :slot:
        """
        self._write_scancode(YK_SCAN_CODE, slot, 'h:000000000000', current_access_code)
        time.sleep1
        cfg = self.key.init_config(zap=True)
        self._write_cfg(cfg, slot)

    def clear(self, current_access_code):
        """
        clear/reset all slots in the device
        """
        for slot in self.enabled_slots():
            self.reset_slot(slot, current_access_code)

    def set_mode(self, slot, mode):
        """
        set operation mode of a slot
        """
        ykcfg = self.key.init_device_config(mode=mode)
        self._write_cfg(ykcfg, slot)

    def set_nfc(self, slot, current_access_code):
        """
        assign NFC to a slot
        """
        if self.key.model == 'YubiKey 4':
            return
        ykcfg_ndef = YubiKeyNEO_NDEF(data=b'', access_code=current_access_code)
        self._write_cfg(ykcfg_ndef, slot=slot)

    def initialize(self, oath_secret, otp_len, oath_tokenid, access_code):
        """
        do the complete initialization of both slots
        """
        self.init_hotp(1, oath_secret, otp_len, oath_tokenid, access_code)
        self.set_nfc(2, access_code.encode'ascii')