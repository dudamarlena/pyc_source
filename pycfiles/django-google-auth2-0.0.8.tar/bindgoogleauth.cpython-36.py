# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth2/google/bindgoogleauth/bindgoogleauth.py
# Compiled at: 2019-04-02 03:10:22
# Size of source mod 2**32: 1167 bytes
from django_google_auth2.models import DjangoGoogleAuthenticator2
import base64, codecs, random, re
from django_google_auth2.utils.googletotp import googletotp

def bind_google_auth(user):
    """
    绑定google令牌
    :param user:  用户邮箱
    :return: google令牌二维码
    """
    queryset_user = DjangoGoogleAuthenticator2.objects.filter(username=user)
    if queryset_user.exists():
        return {'success':False, 
         'data':'{}用户已经绑定google令牌,不能二次绑定'.format(user)}
    else:
        base_32_secret = base64.b32encode(codecs.decode(codecs.encode('{0:020x}'.format(random.getrandbits(80))), 'hex_codec'))
        totp_obj = googletotp.TOTP(base_32_secret.decode('utf-8'))
        qr_code = re.sub('=+$', '', totp_obj.provisioning_uri(user))
        key = str(base_32_secret, encoding='utf-8')
        DjangoGoogleAuthenticator2.objects.create(username=user,
          key=key)
        return {'success':True, 
         'data':qr_code}