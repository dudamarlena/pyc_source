# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ggtool/util/password.py
# Compiled at: 2019-10-20 03:04:21
# Size of source mod 2**32: 329 bytes
import string, random
letters = string.digits + string.ascii_letters

def get_password(num=10):
    """
    获取密码
    :param num: int 字符串长度 default 10
    :return: str
    """
    return ''.join(random.sample(letters, num))


if __name__ == '__main__':
    print(get_password())