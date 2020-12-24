# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/stringutil.py
# Compiled at: 2015-04-04 05:19:06
__doc__ = '\nCreated on 2011-6-15\n字符串帮助类\n@author: huwei\n'
import string, random, hashlib, uuid

def random_string(length=8):
    u"""生成随机字符串.

    :param length:随机字符串长度，默认为8
    :return: 返回随机字符串
    """
    return ('').join(random.sample(string.ascii_letters + string.digits, length))


def random_number(length=6):
    u"""生成随机数字.

    :param length:随机字符串长度，默认为8
    :return: 返回随机字符串
    """
    return ('').join(random.sample(string.digits, length))


def convert_to_utf8(s):
    u"""非UTF8字符串.

    :param s: 转换成UTF8字符串.
    :return: UTF8字符串.
    """
    return s.encode('utf8')


def addslashes(s):
    d = {'"': '\\"', "'": "\\'", '\x00': '\\\x00', '\\': '\\\\'}
    return ('').join(d.get(c, c) for c in s)


def md5(s):
    return hashlib.md5(s).hexdigest()


def uuid4():
    u"""生成uuid4的字符串
    :return:
    """
    return str(uuid.uuid4())


def get_first_char(src):
    first_char_ord = ord(src[0].upper())
    if first_char_ord >= 65 and first_char_ord <= 91 or first_char_ord >= 48 and first_char_ord <= 57:
        return src[0].upper()
    target = src.encode('GB18030')
    asc = ord(target[0]) * 256 + ord(target[1]) - 65536
    if asc >= -20319 and asc <= -20284:
        return 'A'
    if asc >= -20283 and asc <= -19776:
        return 'B'
    if asc >= -19775 and asc <= -19219:
        return 'C'
    if asc >= -19218 and asc <= -18711:
        return 'D'
    if asc >= -18710 and asc <= -18527:
        return 'E'
    if asc >= -18526 and asc <= -18240:
        return 'F'
    if asc >= -18239 and asc <= -17923:
        return 'G'
    if asc >= -17922 and asc <= -17418:
        return 'H'
    if asc >= -17417 and asc <= -16475:
        return 'J'
    if asc >= -16474 and asc <= -16213:
        return 'K'
    if asc >= -16212 and asc <= -15641:
        return 'L'
    if asc >= -15640 and asc <= -15166:
        return 'M'
    if asc >= -15165 and asc <= -14923:
        return 'N'
    if asc >= -14922 and asc <= -14915:
        return 'O'
    if asc >= -14914 and asc <= -14631:
        return 'P'
    if asc >= -14630 and asc <= -14150:
        return 'Q'
    if asc >= -14149 and asc <= -14091:
        return 'R'
    if asc >= -14090 and asc <= -13119:
        return 'S'
    if asc >= -13118 and asc <= -12839:
        return 'T'
    if asc >= -12838 and asc <= -12557:
        return 'W'
    if asc >= -12556 and asc <= -11848:
        return 'X'
    if asc >= -11847 and asc <= -11056:
        return 'Y'
    if asc >= -11055 and asc <= -10247:
        return 'Z'
    if asc == -9767:
        return 'D'
    if asc == -9743 or asc == -6155:
        return 'H'
    if asc == -3372:
        return 'J'
    if asc == -6993 or asc == -6928 or asc == -2633 or asc == -7182:
        return 'L'
    if asc == -6745:
        return 'P'
    if asc == -7703:
        return 'Q'
    if asc == -7725:
        return 'S'
    if asc == -5128:
        return 'T'
    if asc == -8962 or asc == -9744:
        return 'Y'
    if asc == -6973:
        return 'Z'
    print asc
    return ''


if __name__ == '__main__':
    print get_first_char('珲春')
    print get_first_char('浏')
    print get_first_char('醴陵')
    print get_first_char('衢州')
    print get_first_char('泸州')
    print get_first_char('滕州')
    print get_first_char('兖州')
    print get_first_char('蛟河')
    print get_first_char('荥阳')
    print get_first_char('濮阳')
    print get_first_char('涿州')
    print get_first_char('亳州')
    print get_first_char('漯河')
    print get_first_char('儋州')
    print get_first_char('嵊州市')
    print get_first_char('万州')
    print len('c')
    print get_first_char('mark')
    print convert_to_utf8('中国')
    print random_string(8)
    print ('漯河,万州,').split(',')
    print ('万州').split(',')