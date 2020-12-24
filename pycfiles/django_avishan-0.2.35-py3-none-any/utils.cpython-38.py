# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/utils.py
# Compiled at: 2020-04-21 05:34:59
# Size of source mod 2**32: 13015 bytes
import datetime
from typing import Optional, Union, List
from django.http import HttpResponse
from avishan.exceptions import AuthException, AvishanException
from avishan.misc.bch_datetime import BchDatetime
from . import current_request
from .configure import get_avishan_config
from .misc import status
from .models import AuthenticationType

class AvishanDataValidator:

    class ValidatorException(AvishanException):
        from avishan.misc.translation import AvishanTranslatable

        def __init__(self, field_name):
            from avishan.misc.translation import AvishanTranslatable
            current_request['response']['error_in_field'] = field_name
            current_request['response']['error_message'] = AvishanTranslatable(EN=f'"{field_name}" not accepted',
              FA=('"' + field_name + '" قابل قبول نیست'))
            current_request['status_code'] = status.HTTP_417_EXPECTATION_FAILED
            super().__init__()

    @classmethod
    def validate_phone_number(cls, input: str, country_code: str='98', phone_start_number: str='09') -> str:
        from avishan.misc.translation import AvishanTranslatable
        input = en_numbers(input)
        input = input.replace(' ', '')
        input = input.replace('-', '')
        if input.startswith('00'):
            if not input.startswith('00' + country_code):
                raise cls.ValidatorException(AvishanTranslatable(EN='phone number',
                  FA='شماره موبایل'))
            if input.startswith('00' + country_code + phone_start_number):
                input = '00' + country_code + input[5:]
        elif input.startswith('+'):
            if not input.startswith('+' + country_code):
                raise cls.ValidatorException(AvishanTranslatable(EN='phone number',
                  FA='شماره موبایل'))
            input = '00' + input[1:]
            if input.startswith('00' + country_code + phone_start_number):
                input = '00' + country_code + input[5:]
        elif input.startswith(phone_start_number):
            input = '00' + country_code + input[1:]
        if not (len(input) != 14 or input.isdigit()):
            raise cls.ValidatorException(AvishanTranslatable(EN='phone number',
              FA='شماره موبایل'))
        return input

    @classmethod
    def validate_text(cls, input: str, blank: bool=True) -> str:
        input = input.strip()
        input = fa_numbers(input)
        if not blank:
            if len(input) == 0:
                from avishan.misc.translation import AvishanTranslatable
                raise cls.ValidatorException(AvishanTranslatable(EN='text', FA='متن'))
        return input

    @classmethod
    def validate_recommend_code(cls, input: str) -> str:
        input = cls.validate_text(input)
        input = en_numbers(input)
        input = input.upper()
        return input

    @classmethod
    def validate_first_name(cls, input):
        input = input.strip()
        if has_numbers(input) or len(input) < 2:
            from avishan.misc.translation import AvishanTranslatable
            raise cls.ValidatorException(AvishanTranslatable(EN='first name', FA='نام'))
        return input

    @classmethod
    def validate_last_name(cls, input):
        input = input.strip()
        if has_numbers(input) or len(input) < 2:
            from avishan.misc.translation import AvishanTranslatable
            raise cls.ValidatorException(AvishanTranslatable(EN='last name', FA='نام خانوادگی'))
        return input

    @classmethod
    def validate_ferdowsi_student_id(cls, input):
        input = cls.validate_text(input, blank=False)
        if not input.isdigit():
            from avishan.misc.translation import AvishanTranslatable
            raise cls.ValidatorException(AvishanTranslatable(EN='Student ID', FA='کد دانشجویی'))
        return input

    @classmethod
    def validate_plate(cls, plate_a, plate_b, plate_c, plate_d):
        from avishan.misc.translation import AvishanTranslatable
        plate_a = cls.validate_text((fa_numbers(plate_a)), blank=False)
        plate_b = cls.validate_text((fa_numbers(plate_b)), blank=False)
        plate_c = cls.validate_text((fa_numbers(plate_c)), blank=False)
        plate_d = cls.validate_text((fa_numbers(plate_d)), blank=False)
        if plate_b not in ('ب', 'ج', 'د', 'س', 'ص', 'ط', 'ق', 'ل', 'م', 'ن', 'و', 'ه',
                           'ی', 'الف', 'پ', 'ت', 'ث', 'ز', 'ژ', 'ش', 'ع', 'ف', 'ک',
                           'گ', 'D', 'S', 'd', 's', 'ي'):
            raise cls.ValidatorException(AvishanTranslatable(EN='plate', FA='پلاک'))
        if not (plate_a.isdigit() and plate_c.isdigit() and plate_d.isdigit()):
            raise cls.ValidatorException(AvishanTranslatable(EN='plate', FA='پلاک'))
        return (plate_a, plate_b, plate_c, plate_d)

    @classmethod
    def validate_time(cls, input: dict, name: str) -> datetime.time:
        return datetime.time(int(input['hour']), int(input['minute']))


def discard_monitor(url: str) -> bool:
    """
    checks if request is in check-blacklist
    :param url: request url. If straightly catch from request.path, it comes like: /admin, /api/v1
    :return:
    """
    if url.startswith(tuple(get_avishan_config().NOT_MONITORED_STARTS)):
        return True
    return False


def find_token_in_header--- This code section failed: ---

 L. 150         0  SETUP_FINALLY        58  'to 58'

 L. 151         2  LOAD_GLOBAL              current_request
                4  LOAD_STR                 'request'
                6  BINARY_SUBSCR    
                8  LOAD_ATTR                META
               10  LOAD_STR                 'HTTP_AUTHORIZATION'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'temp'

 L. 152        16  LOAD_GLOBAL              can_be_token
               18  LOAD_FAST                'temp'
               20  LOAD_CONST               6
               22  LOAD_CONST               None
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  CALL_FUNCTION_1       1  ''
               30  POP_JUMP_IF_FALSE    54  'to 54'

 L. 153        32  LOAD_FAST                'temp'
               34  LOAD_CONST               6
               36  LOAD_CONST               None
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  LOAD_GLOBAL              current_request
               44  LOAD_STR                 'token'
               46  STORE_SUBSCR     

 L. 154        48  POP_BLOCK        
               50  LOAD_CONST               True
               52  RETURN_VALUE     
             54_0  COME_FROM            30  '30'
               54  POP_BLOCK        
               56  JUMP_FORWARD         78  'to 78'
             58_0  COME_FROM_FINALLY     0  '0'

 L. 155        58  DUP_TOP          
               60  LOAD_GLOBAL              KeyError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    76  'to 76'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 156        72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            64  '64'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            56  '56'

 L. 158        78  LOAD_CONST               False
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 50


def find_token_in_session--- This code section failed: ---

 L. 166         0  SETUP_FINALLY        42  'to 42'

 L. 167         2  LOAD_GLOBAL              current_request
                4  LOAD_STR                 'request'
                6  BINARY_SUBSCR    
                8  LOAD_ATTR                COOKIES
               10  LOAD_STR                 'token'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'temp'

 L. 168        16  LOAD_GLOBAL              can_be_token
               18  LOAD_FAST                'temp'
               20  CALL_FUNCTION_1       1  ''
               22  POP_JUMP_IF_FALSE    38  'to 38'

 L. 169        24  LOAD_FAST                'temp'
               26  LOAD_GLOBAL              current_request
               28  LOAD_STR                 'token'
               30  STORE_SUBSCR     

 L. 170        32  POP_BLOCK        
               34  LOAD_CONST               True
               36  RETURN_VALUE     
             38_0  COME_FROM            22  '22'
               38  POP_BLOCK        
               40  JUMP_FORWARD         62  'to 62'
             42_0  COME_FROM_FINALLY     0  '0'

 L. 171        42  DUP_TOP          
               44  LOAD_GLOBAL              KeyError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    60  'to 60'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 172        56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            48  '48'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            40  '40'

 L. 174        62  LOAD_CONST               False
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 34


def find_token() -> bool:
    """
    check for token in both session and header
    :return: true if token
    """
    if current_request['request'].path.startswith('/api/v1/login/generate/'):
        return False
    if not find_token_in_header():
        if not find_token_in_session():
            return False
    return True


def can_be_token(text):
    """
    checks entered text can be a token
    :param text:
    :return:
    """
    if len(text) > 0:
        return True
    return False


def add_token_to_response(rendered_response: HttpResponse):
    """
    create new token if needed, else reuse previous
    add token to session if session-based auth, else to response header
    """
    if current_request['json_unsafe']:
        return
    if not current_request['add_token']:
        delete_token_from_request(rendered_response)
    elif not current_request['authentication_object']:
        delete_token_from_request(rendered_response)
    else:
        token = encode_token(current_request['authentication_object'])
        if current_request['is_api']:
            current_request['response']['token'] = token
        else:
            rendered_response.set_cookie('token', token)


def delete_token_from_request(rendered_response=None):
    if current_request['is_api']:
        try:
            del current_request['response']['token']
        except KeyError:
            pass

    else:
        rendered_response.delete_cookie('token')


def encode_token(authentication_object: 'AuthenticationType') -> Optional[str]:
    import jwt
    from datetime import timedelta
    now = BchDatetime()
    token_data = {'at_n':authentication_object.class_name(), 
     'at_id':authentication_object.id, 
     'exp':(now + timedelta(seconds=(authentication_object.user_user_group.user_group.token_valid_seconds))).to_unix_timestamp(), 
     'crt':now.to_unix_timestamp(), 
     'lgn':BchDatetime(authentication_object.last_login).to_unix_timestamp() if authentication_object.last_login else now.to_unix_timestamp()}
    return jwt.encode(token_data, (get_avishan_config().JWT_KEY),
      algorithm='HS256').decode('utf8')


def decode_token():
    import jwt
    if not current_request['token']:
        raise AuthException(AuthException.TOKEN_NOT_FOUND)
    try:
        current_request['decoded_token'] = jwt.decode((current_request['token']),
          (get_avishan_config().JWT_KEY), algorithms=[
         'HS256'])
        current_request['add_token'] = True
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthException(AuthException.TOKEN_EXPIRED)
    except:
        raise AuthException(AuthException.ERROR_IN_TOKEN)


def find_and_check_user():
    """
    Populate current_request object with data from token. Then check for user "active" authorization
    :return:
    """
    from avishan.models import AvishanModel
    if not current_request['decoded_token']:
        AuthException(AuthException.ERROR_IN_TOKEN)
    authentication_type_class = AvishanModel.get_model_with_class_name(current_request['decoded_token']['at_n'])
    try:
        authentication_type_object = authentication_type_class.objects.get(id=(current_request['decoded_token']['at_id']))
        user_user_group = authentication_type_object.user_user_group
    except authentication_type_class.DoesNotExist:
        raise AuthException(AuthException.ACCOUNT_NOT_FOUND)
    else:
        if not user_user_group.is_active:
            raise AuthException(AuthException.GROUP_ACCOUNT_NOT_ACTIVE)
        if not user_user_group.base_user.is_active:
            raise AuthException(AuthException.ACCOUNT_NOT_ACTIVE)
        if BchDatetime(authentication_type_object.last_login).to_unix_timestamp() != current_request['decoded_token']['lgn'] or authentication_type_object.last_logout:
            raise AuthException(AuthException.DEACTIVATED_TOKEN)
        populate_current_request(login_with=authentication_type_object)


def populate_current_request(login_with: 'AuthenticationType'):
    current_request['base_user'] = login_with.user_user_group.base_user
    current_request['user_group'] = login_with.user_user_group.user_group
    current_request['user_user_group'] = login_with.user_user_group
    current_request['authentication_object'] = login_with
    if current_request['language'] is None:
        current_request['language'] = login_with.user_user_group.base_user.language
    current_request['add_token'] = True


def create_avishan_config_file(app_name: str=None):
    """
    MONITORED_APPS_NAMES = []
    NOT_MONITORED_STARTS [
        '/admin', '/static', '/media', '/favicon.ico'
    ]
    JWT_KEY = "" or none if not available
    """
    if app_name:
        f = open(app_name + '/avishan_config.py', 'w+')
    else:
        f = open('avishan_config.py', 'w+')
    f.writelines(('def check():\n', '    pass\n\n\n', 'class AvishanConfig:\n'))
    if not app_name:
        f.writelines([
         '    MONITORED_APPS_NAMES = []\n',
         "    NOT_MONITORED_STARTS = ['/admin', '/static', '/favicon.ico']\n",
         "    JWT_KEY = 'CHANGE_THIS_KEY'\n",
         '    USE_JALALI_DATETIME = True\n'])
    else:
        f.write('    pass\n')
    f.close()


def fa_numbers(text):
    text = str(text)
    text = en_numbers(text)
    array = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    result = ''
    for i in str(text):
        if i.isdigit():
            result = result + array[int(i)]
        else:
            result = result + i
    else:
        return result


def en_numbers(text):
    text = str(text)
    result = ''
    array = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    for char in text:
        if char in array:
            result += str(array.index(char))
        else:
            result += char
    else:
        return result


def has_numbers(input):
    return any((char.isdigit() for char in input))


def find_file(name: str, parent_directory_path: str) -> List[str]:
    import os
    result = []
    for root, dirs, files in os.walk(parent_directory_path):
        if name in files:
            result.append(os.path.join(root, name))
        return result


def all_subclasses(parent_class):
    return list(set(parent_class.__subclasses__()).union([s for c in parent_class.__subclasses__() for s in all_subclasses(c)]))


def parse_url(url: str):
    from urllib.parse import urlparse
    return urlparse(url)