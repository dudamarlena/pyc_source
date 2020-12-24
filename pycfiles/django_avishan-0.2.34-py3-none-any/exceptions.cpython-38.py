# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/exceptions.py
# Compiled at: 2020-04-27 02:42:50
# Size of source mod 2**32: 7608 bytes
from typing import Optional, Union, List
from . import current_request
from .misc import status
from misc.translation import AvishanTranslatable

class AvishanException(Exception):

    def __init__(self, wrap_exception: Optional[Exception]=None, status_code: int=status.HTTP_400_BAD_REQUEST):
        save_traceback()
        if wrap_exception:
            if isinstance(wrap_exception, KeyError):
                body = f"field {wrap_exception.args[0]} not found in data and its required"
            else:
                body = str(wrap_exception.args[0]) if len(wrap_exception.args) == 1 else str(wrap_exception.args)
            current_request['exception'] = wrap_exception
            current_request['status_code'] = status.HTTP_418_IM_TEAPOT
            add_error_message_to_response(body=body)
        else:
            current_request['exception'] = self
            current_request['status_code'] = status_code


class AuthException(AvishanException):
    from misc.translation import AvishanTranslatable
    NOT_DEFINED = (
     0, AvishanTranslatable(EN='Not Defined', FA='مشخص نشده'))
    ACCOUNT_NOT_FOUND = (1, AvishanTranslatable(EN='User Account not found', FA='حساب کاربری پیدا نشد'))
    ACCOUNT_NOT_ACTIVE = (2, AvishanTranslatable(EN='Deactivated User Account', FA='حساب کاربری غیرفعال است'))
    GROUP_ACCOUNT_NOT_ACTIVE = (3,
     AvishanTranslatable(EN='User Account Deactivated in Selected User Group',
       FA='حساب کاربری در گروه\u200cکاربری انتخاب شده غیر فعال است'))
    TOKEN_NOT_FOUND = (
     4, AvishanTranslatable(EN='Token not found', FA='توکن پیدا نشد'))
    TOKEN_EXPIRED = (5, AvishanTranslatable(EN='Token timed out', FA='زمان استفاده از توکن تمام شده است'))
    ERROR_IN_TOKEN = (6, AvishanTranslatable(EN='Error in token', FA='خطا در توکن'))
    ACCESS_DENIED = (7, AvishanTranslatable(EN='Access Denied', FA='دسترسی غیرمجاز'))
    HTTP_METHOD_NOT_ALLOWED = (8, AvishanTranslatable(EN='HTTP method not allowed in this url'))
    INCORRECT_PASSWORD = (9, AvishanTranslatable(EN='Incorrect Password', FA='رمز اشتباه است'))
    DUPLICATE_AUTHENTICATION_IDENTIFIER = (10,
     AvishanTranslatable(EN='Authentication Identifier already Exists',
       FA='شناسه احراز هویت تکراری است'))
    DUPLICATE_AUTHENTICATION_TYPE = (
     11,
     AvishanTranslatable(EN='Duplicate Authentication Type for User Account',
       FA='روش احراز هویت برای این حساب کاربری تکراری است'))
    DEACTIVATED_TOKEN = (
     12,
     AvishanTranslatable(EN='Token Deactivated, Sign in again',
       FA='توکن غیرفعال شده است، دوباره وارد شوید'))
    MULTIPLE_CONNECTED_ACCOUNTS = (
     13,
     AvishanTranslatable(EN='Multiple Accounts found with this identifier, Choose user group in url parameter',
       FA='چند حساب با این شناسه پیدا شد، گروه کاربری را در پارامتر url مشخص کنید'))
    METHOD_NOT_DIRECT_CALLABLE = (
     14,
     AvishanTranslatable(EN='Method is not callable direct to model',
       FA='تابع به طور مستقیم قابل صدا زدن نیست'))

    def __init__(self, error_kind=NOT_DEFINED):
        from misc.translation import AvishanTranslatable
        status_code = status.HTTP_403_FORBIDDEN
        self.error_kind = error_kind
        if error_kind[0] == AuthException.HTTP_METHOD_NOT_ALLOWED[0]:
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        super().__init__(status_code=status_code)
        add_error_message_to_response(code=(error_kind[0]), body=(str(error_kind[1])), title=(str(AvishanTranslatable(EN='Authentication Exception',
          FA='خطای احراز هویت'))))

    @classmethod
    def get_login_required_errors(cls) -> List[tuple]:
        return [
         cls.ACCOUNT_NOT_FOUND,
         cls.ACCOUNT_NOT_ACTIVE,
         cls.GROUP_ACCOUNT_NOT_ACTIVE,
         cls.TOKEN_NOT_FOUND,
         cls.TOKEN_EXPIRED,
         cls.ERROR_IN_TOKEN,
         cls.INCORRECT_PASSWORD,
         cls.DEACTIVATED_TOKEN,
         cls.MULTIPLE_CONNECTED_ACCOUNTS]


class ErrorMessageException(AvishanException):

    def __init__(self, message='Error', status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code)
        message = str(message)
        add_error_message_to_response(body=(message if message else 'Error details not provided'),
          title='Error')


def add_debug_message_to_response(body: str=None, title: str=None):
    debug = {}
    if body is not None:
        debug['body'] = body
    if title is not None:
        debug['title'] = title
    current_request['messages']['debug'].append(debug)


def add_info_message_to_response(body: str=None, title: str=None):
    info = {}
    if body is not None:
        info['body'] = body
    if title is not None:
        info['title'] = title
    current_request['messages']['info'].append(info)


def add_success_message_to_response(body: str=None, title: str=None):
    success = {}
    if body is not None:
        success['body'] = body
    if title is not None:
        success['title'] = title
    current_request['messages']['success'].append(success)


def add_warning_message_to_response(body: str=None, title: str=None):
    warning = {}
    if body is not None:
        warning['body'] = body
    if title is not None:
        warning['title'] = title
    current_request['messages']['warning'].append(warning)


def add_error_message_to_response(body: str=None, title: str=None, code=None):
    if 'messages' not in current_request.keys():
        return
    error = {}
    if body is not None:
        error['body'] = body
    if title is not None:
        error['title'] = title
    if code is not None:
        error['code'] = code
    current_request['messages']['error'].append(error)


def save_traceback--- This code section failed: ---

 L. 178         0  SETUP_FINALLY        24  'to 24'

 L. 179         2  LOAD_GLOBAL              current_request
                4  LOAD_STR                 'traceback'
                6  BINARY_SUBSCR    
                8  LOAD_CONST               None
               10  COMPARE_OP               is-not
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L. 180        14  POP_BLOCK        
               16  LOAD_CONST               None
               18  RETURN_VALUE     
             20_0  COME_FROM            12  '12'
               20  POP_BLOCK        
               22  JUMP_FORWARD         46  'to 46'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 181        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 182        38  POP_EXCEPT       
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      
             46_0  COME_FROM            22  '22'

 L. 183        46  LOAD_CONST               0
               48  LOAD_CONST               None
               50  IMPORT_NAME              sys
               52  STORE_FAST               'sys'
               54  LOAD_CONST               0
               56  LOAD_CONST               None
               58  IMPORT_NAME              traceback
               60  STORE_FAST               'traceback'

 L. 184        62  LOAD_FAST                'sys'
               64  LOAD_METHOD              exc_info
               66  CALL_METHOD_0         0  ''
               68  UNPACK_SEQUENCE_3     3 
               70  STORE_FAST               'exc_type'
               72  STORE_FAST               'exc_value'
               74  STORE_FAST               'exc_tb'

 L. 185        76  LOAD_FAST                'traceback'
               78  LOAD_METHOD              TracebackException

 L. 186        80  LOAD_FAST                'exc_type'

 L. 186        82  LOAD_FAST                'exc_value'

 L. 186        84  LOAD_FAST                'exc_tb'

 L. 185        86  CALL_METHOD_3         3  ''
               88  STORE_FAST               'tbe'

 L. 188        90  LOAD_FAST                'tbe'
               92  LOAD_ATTR                exc_traceback
               94  LOAD_CONST               None
               96  COMPARE_OP               is-not
               98  POP_JUMP_IF_FALSE   164  'to 164'

 L. 189       100  LOAD_STR                 ''
              102  LOAD_METHOD              join
              104  LOAD_FAST                'tbe'
              106  LOAD_METHOD              format
              108  CALL_METHOD_0         0  ''
              110  CALL_METHOD_1         1  ''
              112  LOAD_GLOBAL              current_request
              114  LOAD_STR                 'traceback'
              116  STORE_SUBSCR     

 L. 190       118  LOAD_GLOBAL              print
              120  LOAD_GLOBAL              current_request
              122  LOAD_STR                 'traceback'
              124  BINARY_SUBSCR    
              126  CALL_FUNCTION_1       1  ''
              128  POP_TOP          

 L. 191       130  LOAD_GLOBAL              current_request
              132  LOAD_STR                 'exception_record'
              134  BINARY_SUBSCR    
              136  POP_JUMP_IF_FALSE   164  'to 164'

 L. 192       138  LOAD_GLOBAL              current_request
              140  LOAD_STR                 'traceback'
              142  BINARY_SUBSCR    
              144  LOAD_GLOBAL              current_request
              146  LOAD_STR                 'exception_record'
              148  BINARY_SUBSCR    
              150  STORE_ATTR               traceback

 L. 193       152  LOAD_GLOBAL              current_request
              154  LOAD_STR                 'exception_record'
              156  BINARY_SUBSCR    
              158  LOAD_METHOD              save
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          
            164_0  COME_FROM           136  '136'
            164_1  COME_FROM            98  '98'

Parse error at or near `LOAD_CONST' instruction at offset 16