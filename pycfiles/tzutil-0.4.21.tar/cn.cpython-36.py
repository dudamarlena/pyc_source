# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/txt/cn.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 1808 bytes


def has_chinese(s):
    for i in s:
        if i >= '一':
            if i <= '龥':
                return True

    return False


def 全角转半角(ustring):
    rstring = []
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
            uchar = 0
        else:
            if inside_code >= 65281:
                if inside_code <= 65374:
                    inside_code -= 65248
                    uchar = 0
        rstring.append(uchar or chr(inside_code))

    return ''.join(rstring)


def 去空格(s):
    if s:
        return s.strip('\n\r\xa0 \xa0\u3000')


def 短句窗口(s):
    for line in s.replace('。', '\n').replace('?', '\n').replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        r = []
        count = 0
        for i in 按标点分割(line):
            count += len(i)
            r.append(i)
            if count > 5:
                yield ''.join(r)
                count = 0
                r = []

        if count > 5:
            yield ''.join(r)


连字符 = '.-/&'

def 按标点分割(s):
    r = []
    for i in s + ' ':
        if i >= '一' and i <= '龥' or i.isalnum() or i in 连字符:
            r.append(i)
        else:
            s = 去空格(''.join(r))
            if s:
                if s not in 连字符:
                    yield s
            r = []


def 去标点(s):
    return ''.join(按标点分割(s))


def chinese_count(s):
    count = 0
    for i in s:
        if i >= '一' and i <= '龥':
            count += 1

    return count


def chinese_more_than(s, max_count):
    count = 0
    for i in s:
        if i >= '一':
            if i <= '龥':
                count += 1
                if count > max_count:
                    return True