# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\network.py
# Compiled at: 2020-04-04 22:35:59
# Size of source mod 2**32: 3455 bytes
"""Network"""
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import shaonutil, urllib.parse, re, requests, wget, socket, sys

def check_port--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              socket
                2  LOAD_METHOD              socket
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               's'

 L.  21         8  LOAD_FAST                'log'
               10  POP_JUMP_IF_FALSE    28  'to 28'

 L.  21        12  LOAD_GLOBAL              print
               14  LOAD_STR                 'Attempting to connect to %s on port %s'
               16  LOAD_FAST                'address'
               18  LOAD_FAST                'port'
               20  BUILD_TUPLE_2         2 
               22  BINARY_MODULO    
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          
             28_0  COME_FROM            10  '10'

 L.  22        28  SETUP_FINALLY       148  'to 148'
               30  SETUP_FINALLY        76  'to 76'

 L.  23        32  LOAD_FAST                's'
               34  LOAD_METHOD              connect
               36  LOAD_FAST                'address'
               38  LOAD_FAST                'port'
               40  BUILD_TUPLE_2         2 
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L.  24        46  LOAD_FAST                'log'
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L.  24        50  LOAD_GLOBAL              print
               52  LOAD_STR                 'Connected to %s on port %s'
               54  LOAD_FAST                'address'
               56  LOAD_FAST                'port'
               58  BUILD_TUPLE_2         2 
               60  BINARY_MODULO    
               62  CALL_FUNCTION_1       1  ''
               64  POP_TOP          
             66_0  COME_FROM            48  '48'

 L.  25        66  POP_BLOCK        
               68  POP_BLOCK        
               70  CALL_FINALLY        148  'to 148'
               72  LOAD_CONST               True
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    30  '30'

 L.  26        76  DUP_TOP          
               78  LOAD_GLOBAL              socket
               80  LOAD_ATTR                error
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE   142  'to 142'
               86  POP_TOP          
               88  STORE_FAST               'e'
               90  POP_TOP          
               92  SETUP_FINALLY       130  'to 130'

 L.  27        94  LOAD_FAST                'log'
               96  POP_JUMP_IF_FALSE   116  'to 116'

 L.  27        98  LOAD_GLOBAL              print
              100  LOAD_STR                 'Connection to %s on port %s failed: %s'
              102  LOAD_FAST                'address'
              104  LOAD_FAST                'port'
              106  LOAD_FAST                'e'
              108  BUILD_TUPLE_3         3 
              110  BINARY_MODULO    
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          
            116_0  COME_FROM            96  '96'

 L.  28       116  POP_BLOCK        
              118  POP_EXCEPT       
              120  CALL_FINALLY        130  'to 130'
              122  POP_BLOCK        
              124  CALL_FINALLY        148  'to 148'
              126  LOAD_CONST               False
              128  RETURN_VALUE     
            130_0  COME_FROM           120  '120'
            130_1  COME_FROM_FINALLY    92  '92'
              130  LOAD_CONST               None
              132  STORE_FAST               'e'
              134  DELETE_FAST              'e'
              136  END_FINALLY      
              138  POP_EXCEPT       
              140  JUMP_FORWARD        144  'to 144'
            142_0  COME_FROM            84  '84'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM           124  '124'
            148_1  COME_FROM            70  '70'
            148_2  COME_FROM_FINALLY    28  '28'

 L.  30       148  LOAD_FAST                's'
              150  LOAD_METHOD              close
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          
              156  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 68


def urlExist(url):
    """Check if the file exist in online"""
    res = requests.headurl
    if res.ok:
        return True
    return False


def downloadFile(url, filename):
    """Donwload a file if error occurs returns false"""
    if urlExist(url):
        wget.download(url, filename)
        return True
    return False


def url_encoding_to_utf_8(url):
    """url_encoding_to_utf_8(url)"""
    url = urllib.parse.unquoteurl
    return url


def check_valid_url(url):
    regex = re.compile('^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}\\.?)|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


class Email:

    def __init__(self):
        self._authentication = ''

    @property
    def authentication(self):
        return self._authentication

    @authentication.setter
    def authentication(self, new_value):
        self._authentication = new_value

    def send_email--- This code section failed: ---

 L.  81         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _authentication
                4  LOAD_STR                 'smtp_server'
                6  BINARY_SUBSCR    
                8  STORE_FAST               'smtp_server'

 L.  82        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _authentication
               14  LOAD_STR                 'smtp_port'
               16  BINARY_SUBSCR    
               18  STORE_FAST               'smtp_port'

 L.  83        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _authentication
               24  LOAD_STR                 'smtp_username'
               26  BINARY_SUBSCR    
               28  STORE_FAST               'sender_address'

 L.  84        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _authentication
               34  LOAD_STR                 'smtp_password'
               36  BINARY_SUBSCR    
               38  STORE_FAST               'sender_pass'

 L.  86        40  LOAD_FAST                'receiver_address'
               42  STORE_FAST               'receiver_address'

 L.  89        44  LOAD_GLOBAL              MIMEMultipart
               46  CALL_FUNCTION_0       0  ''
               48  STORE_FAST               'message'

 L.  90        50  LOAD_FAST                'sender_address'
               52  LOAD_FAST                'message'
               54  LOAD_STR                 'From'
               56  STORE_SUBSCR     

 L.  91        58  LOAD_FAST                'receiver_address'
               60  LOAD_FAST                'message'
               62  LOAD_STR                 'To'
               64  STORE_SUBSCR     

 L.  92        66  LOAD_FAST                'subject'
               68  LOAD_FAST                'message'
               70  LOAD_STR                 'Subject'
               72  STORE_SUBSCR     

 L.  94        74  LOAD_FAST                'message'
               76  LOAD_METHOD              attach
               78  LOAD_GLOBAL              MIMEText
               80  LOAD_FAST                'mail_content'
               82  LOAD_STR                 'plain'
               84  CALL_FUNCTION_2       2  ''
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.  96        90  LOAD_GLOBAL              smtplib
               92  LOAD_METHOD              SMTP
               94  LOAD_FAST                'smtp_server'
               96  LOAD_FAST                'smtp_port'
               98  CALL_METHOD_2         2  ''
              100  STORE_FAST               'session'

 L.  97       102  LOAD_FAST                'session'
              104  LOAD_METHOD              starttls
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L.  99       110  SETUP_FINALLY       128  'to 128'

 L. 100       112  LOAD_FAST                'session'
              114  LOAD_METHOD              login
              116  LOAD_FAST                'sender_address'
              118  LOAD_FAST                'sender_pass'
              120  CALL_METHOD_2         2  ''
              122  POP_TOP          
              124  POP_BLOCK        
              126  JUMP_FORWARD        192  'to 192'
            128_0  COME_FROM_FINALLY   110  '110'

 L. 101       128  DUP_TOP          
              130  LOAD_GLOBAL              smtplib
              132  LOAD_ATTR                SMTPAuthenticationError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   190  'to 190'
              138  POP_TOP          
              140  STORE_FAST               'e'
              142  POP_TOP          
              144  SETUP_FINALLY       178  'to 178'

 L. 103       146  LOAD_FAST                'log'
              148  POP_JUMP_IF_FALSE   158  'to 158'

 L. 103       150  LOAD_GLOBAL              print
              152  LOAD_STR                 'if using gmail smtp, check server host,port\n  if user/pass is not accepeted , turn on less secure app setting and recognize the activity warning mail sent in your gmail, then it will send email in next run.'
              154  CALL_FUNCTION_1       1  ''
              156  POP_TOP          
            158_0  COME_FROM           148  '148'

 L. 104       158  LOAD_GLOBAL              str
              160  LOAD_FAST                'e'
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'stat_message'

 L. 105       166  LOAD_FAST                'stat_message'
              168  ROT_FOUR         
              170  POP_BLOCK        
              172  POP_EXCEPT       
              174  CALL_FINALLY        178  'to 178'
              176  RETURN_VALUE     
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM_FINALLY   144  '144'
              178  LOAD_CONST               None
              180  STORE_FAST               'e'
              182  DELETE_FAST              'e'
              184  END_FINALLY      
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           136  '136'
              190  END_FINALLY      
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           126  '126'

 L. 108       192  LOAD_FAST                'message'
              194  LOAD_METHOD              as_string
              196  CALL_METHOD_0         0  ''
              198  STORE_FAST               'text'

 L. 109       200  LOAD_FAST                'session'
              202  LOAD_METHOD              sendmail
              204  LOAD_FAST                'sender_address'
              206  LOAD_FAST                'receiver_address'
              208  LOAD_FAST                'text'
              210  CALL_METHOD_3         3  ''
              212  POP_TOP          

 L. 110       214  LOAD_FAST                'session'
              216  LOAD_METHOD              quit
              218  CALL_METHOD_0         0  ''
              220  POP_TOP          

 L. 111       222  LOAD_STR                 'Mail Sent'
              224  STORE_FAST               'stat_message'

 L. 112       226  LOAD_FAST                'stat_message'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 170


if __name__ == '__main__':
    pass