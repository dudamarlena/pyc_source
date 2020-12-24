# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/fileutil.py
# Compiled at: 2015-04-04 05:19:06
__doc__ = '\nCreated on 2011-8-15\n\n@author: huwei\n'
import os.path
from string import lower
from app.commons import dateutil
base = [ str(x) for x in range(10) ] + [ chr(x) for x in range(ord('a'), ord('z')) ]

def force_mkdir(path):
    if not os.path.exists(path):
        force_mkdir(os.path.dirname(path))
        os.mkdir(path)


def is_image_extention(filename):
    imgexts = [
     'jpg', 'gif', 'jpeg', 'png']
    if filename is None:
        return False
    else:
        file_info = os.path.splitext(filename)
        if len(file_info) != 2:
            return False
        try:
            e = lower(file_info[1][1:])
            return imgexts.index(e) > -1
        except ValueError:
            return False

        return


def base_convert(n, base):
    """convert decimal integer n to equivalent string in another base (2-36)"""
    if base < 2 or base > 36:
        raise NotImplementedError
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    sign = ''
    if n == 0:
        return '0'
    if n < 0:
        sign = '-'
        n = -n
    s = ''
    while n != 0:
        r = n % base
        s = digits[r] + s
        n = n // base

    return sign + s


def get_write_file_name(filesize, ext=None):
    temp = long(dateutil.timestamp())
    one_path = base_convert(divmod(temp, 100)[1], 36)
    two_path = base_convert(divmod(temp / 100, 1000)[1], 36)
    if ext:
        return one_path + '/' + two_path + '/' + base_convert(temp, 36) + base_convert(filesize, 36) + '.' + ext
    return one_path + '/' + two_path + '/' + base_convert(temp, 36) + base_convert(filesize, 36)


if __name__ == '__main__':
    print get_write_file_name(343454, 'jpg')