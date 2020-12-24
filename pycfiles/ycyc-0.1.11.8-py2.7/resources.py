# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/base/resources.py
# Compiled at: 2016-02-25 04:17:16


class Regex(object):

    @classmethod
    def chinese_word(cls):
        return '[\\u4e00-\\u9fa5]'

    @classmethod
    def email_addr(cls):
        return "[\\w!#$%&'*+/=?^_`{|}~-]+(?:\\.[\\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\\w](?:[\\w-]*[\\w])?\\.)+[\\w](?:[\\w-]*[\\w])?"

    @classmethod
    def date(cls):
        return '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'

    @classmethod
    def humanable_time(cls):
        """
        ref: https://www.debuggex.com/r/eZ4di-IwrKFs8Jns
        """
        return '(?:(?:0?[1-9]|1[0-2])(?::|\\.)[0-5][0-9](?:(?::|\\.)[0-5][0-9])? ?[aApP][mM])|(?:(?:0?[0-9]|1[0-9]|2[0-3])(?::|\\.)[0-5][0-9](?:(?::|\\.)[0-5][0-9])?)'

    @classmethod
    def hms_time(cls):
        """
        ref: https://www.debuggex.com/r/hKCyOSz-VJqO0G8d
        """
        return '(0?[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])'

    @classmethod
    def simple_url_pattern(cls):
        return '\\b\\w+://([\\w\\-\\(\\)]+[\\.@:/]*){3,}(\\?[\\w=\\+%&~;\\*\\-\\.]+)*(#[\\w\\S]+)*\\b'

    @classmethod
    def fully_url_pattern(cls):
        return "([a-z]([a-z]|\\d|\\+|-|\\.)*):(\\/\\/(((([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:)*@)?((\\[(|(v[\\da-f]{1,}\\.(([a-z]|\\d|-|\\.|_|~)|[!\\$&'\\(\\)\\*\\+,;=]|:)+))\\])|((\\d|[1-9]\\d|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d|[1-9]\\d|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d|[1-9]\\d|1\\d\\d|2[0-4]\\d|25[0-5])\\.(\\d|[1-9]\\d|1\\d\\d|2[0-4]\\d|25[0-5]))|(([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=])*)(:\\d*)?)(\\/(([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)*)*|(\\/((([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)+(\\/(([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)*)*)?)|((([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)+(\\/(([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)*)*)|((([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)){0})(\\?((([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)|[\\xE000-\\xF8FF]|\\/|\\?)*)?(\\#((([a-z]|\\d|-|\\.|_|~|[\\x00A0-\\xD7FF\\xF900-\\xFDCF\\xFDF0-\\xFFEF])|(%[\\da-f]{2})|[!\\$&'\\(\\)\\*\\+,;=]|:|@)|\\/|\\?)*)?"

    @classmethod
    def quoted_string(cls, q_mark='"'):
        return ('{q}((?:\\\\.|[^{q}\\\\])*){q}').format(q=q_mark)

    @classmethod
    def variabl_name(cls):
        return '[_a-zA-Z]\\w*'

    @classmethod
    def hex_num(cls, repeat=1):
        return cls.pattern_repeat('[0-9A-Fa-f]', repeat)

    @classmethod
    def pattern_repeat(cls, pattern, end, start=1):
        if end is None:
            if start == 0:
                return '(?:%s)*' % pattern
            if start == 1:
                return '(?:%s)+' % pattern
        if end == 1:
            if start == 1:
                return pattern
            if start == 0:
                return '(?:%s)?' % pattern
        if end > start:
            return '(?:%s){%s,%s}' % (pattern, start, end)
        else:
            if end < start:
                return ''
            if end > 0:
                return '(?:%s){%s}' % (pattern, end)
            return ''

    @classmethod
    def num_less_than(cls, num):

        def up_to(end, start=0):
            if end == 9 and start == 0:
                return '\\d'
            if end > start:
                return '[%s-%s]' % (start, end)
            if end < start:
                return ''
            return '%s' % end

        if num <= 0:
            raise ValueError()
        if num < 10:
            return up_to(num - 1, 0)
        str_n = str(num)
        len_n = len(str_n)
        pattern_set = {
         cls.pattern_repeat(up_to(9, 0), len_n - 1)}
        l_pattern = ''
        for i, n in enumerate(str_n):
            n = int(n)
            repeats = len_n - 1 - i
            h_up_to = up_to(n - 1, 0 if i > 0 else 1)
            if n > 0 and h_up_to:
                pattern_set.add('%s%s%s' % (
                 l_pattern,
                 h_up_to,
                 cls.pattern_repeat(up_to(9, 0), repeats, repeats)))
            l_pattern += str(n)

        return '(?:%s)' % ('|').join(pattern_set)

    @classmethod
    def ipv4(cls):
        ip_field = '0*%s' % cls.num_less_than(256)
        return '(?<!\\d)(%s(?:\\.%s){3})(?!\\d)' % (ip_field, ip_field)