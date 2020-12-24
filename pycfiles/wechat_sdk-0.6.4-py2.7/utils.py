# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/utils.py
# Compiled at: 2016-04-12 23:03:20
import io, six, time, random

def to_text(value, encoding='utf-8'):
    u"""将 value 转为 unicode，默认编码 utf-8

    :param value: 待转换的值
    :param encoding: 编码
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    u"""将 values 转为 bytes，默认编码 utf-8

    :param value: 待转换的值
    :param encoding: 编码
    """
    if not value:
        return ''
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    if six.PY3:
        return six.binary_type(str(value), encoding)
    return six.binary_type(value)


def disable_urllib3_warning():
    u"""
    https://urllib3.readthedocs.org/en/latest/security.html#insecurerequestwarning
    InsecurePlatformWarning 警告的临时解决方案
    """
    try:
        import requests.packages.urllib3
        requests.packages.urllib3.disable_warnings()
    except Exception:
        pass


def generate_timestamp():
    u"""生成 timestamp
    :return: timestamp string
    """
    return int(time.time())


def generate_nonce():
    u"""生成 nonce
    :return: nonce string
    """
    return random.randrange(1000000000, 2000000000)


def convert_ext_to_mime(extension):
    u"""将扩展名转换为 MIME 格式
    :return: mime string
    """
    table = {'jpg': 'image/jpeg', 
       'jpeg': 'image/jpeg', 
       'amr': 'audio/amr', 
       'mp3': 'audio/mpeg', 
       'mp4': 'video/mp4'}
    if extension in table:
        return table[extension]
    raise ValueError('Invalid extension in MIME table')


def is_allowed_extension(extension, type='upload_media'):
    u"""检查扩展名是否是可以上传到服务器
    :return: True if ok
    """
    table = ('jpg', 'jpeg', 'amr', 'mp3', 'mp4')
    if extension in table:
        return True
    return False