# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/convert2-project/convert2/pkg/rolex/parse.py
# Compiled at: 2018-01-22 18:09:34
# Size of source mod 2**32: 9230 bytes
from datetime import date, datetime
from dateutil.parser import parse
try:
    from .pkg import sixmini
    from .util import from_ordinal, from_utctimestamp
except:
    from rolex.pkg import sixmini
    from rolex.util import from_ordinal, from_utctimestamp

date_template_and_example = [
 ('%Y-%m-%d', '2014-09-20'),
 ('%m-%d-%Y', '09-20-2014'),
 ('%Y/%m/%d', '2014/09/20'),
 ('%m/%d/%Y', '09/20/2014'),
 ('%Y.%m.%d', '2014.09.20'),
 ('%m.%d.%Y', '9.20.2014'),
 ('%B %d, %Y', 'September 20, 2014'),
 ('%A, %B %d, %Y', 'Saturday, September 20, 2014'),
 ('%b %d, %Y', 'Sep 20, 2014'),
 ('%a, %b %d, %Y', 'Sat, Sep 20, 2014'),
 ('%Y%m%d', '20140920'),
 ('%y%m%d', '140920'),
 ('%m%d%Y', '09202014'),
 ('%m%d%y', '092014')]
date_template_list = [tpl for tpl, example in date_template_and_example]
datetime_template_and_example = [
 ('%Y-%m-%d %H:%M:%S', '2014-01-15 17:58:31'),
 ('%Y-%m-%d %H:%M:%S.%f', '2014-01-15 17:58:31.1234'),
 ('%Y-%m-%d %H:%M', '2014-01-15 17:58'),
 ('%Y-%m-%d %I:%M:%S %p', '2014-01-15 5:58:31 PM'),
 ('%Y-%m-%d %I:%M %p', '2014-01-15 05:58 PM'),
 ('%Y-%m-%d %I %p', '2014-01-15 05 PM'),
 ('%m-%d-%Y %H:%M:%S', '1-15-2014 17:58:31'),
 ('%m-%d-%Y %H:%M:%S.%f', '1-15-2014 17:58:31.1234'),
 ('%m-%d-%Y %H:%M', '1-15-2014 17:58'),
 ('%m-%d-%Y %I:%M:%S %p', '1-15-2014 5:58:31 PM'),
 ('%m-%d-%Y %I:%M %p', '1-15-2014 05:58 PM'),
 ('%m-%d-%Y %I %p', '1-15-2014 05 PM'),
 ('%Y/%m/%d %H:%M:%S', '2014/01/15 17:58:31'),
 ('%Y/%m/%d %H:%M:%S.%f', '2014/01/15 17:58:31.1234'),
 ('%Y/%m/%d %H:%M', '2014/01/15 17:58'),
 ('%Y/%m/%d %I:%M:%S %p', '2014/01/15 5:58:31 PM'),
 ('%Y/%m/%d %I:%M %p', '2014/01/15 05:58 PM'),
 ('%Y/%m/%d %I %p', '2014/01/15 05 PM'),
 ('%m/%d/%Y %H:%M:%S', '1/15/2014 17:58:31'),
 ('%m/%d/%Y %H:%M:%S.%f', '1/15/2014 17:58:31.1234'),
 ('%m/%d/%Y %H:%M', '1/15/2014 17:58'),
 ('%m/%d/%Y %I:%M:%S %p', '1/15/2014 5:58:31 PM'),
 ('%m/%d/%Y %I:%M %p', '1/15/2014 05:58 PM'),
 ('%m/%d/%Y %I %p', '1/15/2014 05 PM'),
 ('%H:%M:%S %m/%d/%Y', '17:58:31 1/15/2014'),
 ('%H:%M:%S.%f %m/%d/%Y', '17:58:31.1234 1/15/2014'),
 ('%H:%M %m/%d/%Y', '17:58 1/15/2014'),
 ('%I:%M:%S %p %m/%d/%Y', '5:58:31 PM 1/15/2014'),
 ('%I:%M %p %m/%d/%Y', '05:58 PM 1/15/2014'),
 ('%I %p %m/%d/%Y', '05 PM 1/15/2014'),
 ('%Y%m%d%H', '2014011506'),
 ('%Y%m%d%H%M', '201401150630'),
 ('%Y%m%d%H%M%S', '20140115063015'),
 ('%Y%m%d%H%M%S.%f', '20140115063015.123'),
 ('%y%m%d%H', '14011506'),
 ('%y%m%d%H%M', '1401150630'),
 ('%y%m%d%H%M%S', '140115063015'),
 ('%y%m%d%H%M%S.%f', '140115063015.123'),
 ('%Y-%m-%dT%H:%M:%S', '2014-01-15T17:58:31'),
 ('%Y-%m-%dT%H:%M:%S.%f', '2014-01-15T17:58:31.1234'),
 ('%Y-%m-%dT%H:%M:%SZ%Z', '2014-01-15T17:58:31ZUTC'),
 ('%Y-%m-%dT%H:%M:%S.%fZ%Z', '2014-01-15T17:58:31.1234ZUTC'),
 ('%a, %d %b %Y %H:%M:%S GMT', 'Wed, 15 Jan 2014 17:58:31 GMT')]
if sixmini.PY3:
    datetime_template_and_example.extend([
     ('%Y-%m-%dT%H:%M:%SZ%z', '2014-01-15T17:58:31Z-0400'),
     ('%Y-%m-%dT%H:%M:%S.%fZ%z', '2014-01-15T17:58:31.1234Z-0400')])
datetime_template_and_example.extend(date_template_and_example)
datetime_template_list = [tpl for tpl, example in datetime_template_and_example]

class Parser(object):
    """Parser"""
    _default_date_template = date_template_list[0]
    _default_datetime_template = datetime_template_list[0]

    def str2date(self, date_str):
        """
        Parse date from string.

        If there's no template matches your string, Please go
        https://github.com/MacHu-GWU/rolex-project/issues
        submit your datetime string. I 'll update templates ASAP.

        This method is faster than :meth:`dateutil.parser.parse`.

        :param date_str: a string represent a date
        :type date_str: str
        :return: a date object

        **中文文档**

        从string解析date。首先尝试默认模板, 如果失败了, 则尝试所有的模板。
        一旦尝试成功, 就将当前成功的模板保存为默认模板。这样做在当你待解析的
        字符串非常多, 且模式单一时, 只有第一次尝试耗时较多, 之后就非常快了。
        该方法要快过 :meth:`dateutil.parser.parse` 方法。
        """
        try:
            a_datetime = datetime.strptime(date_str, self._default_date_template)
            return a_datetime.date()
        except:
            pass

        for template in date_template_list:
            try:
                a_datetime = datetime.strptime(date_str, template)
                self._default_date_template = template
                return a_datetime.date()
            except:
                pass

        raise ValueError('Unable to parse date from: %r!' % date_str)

    def _str2datetime(self, datetime_str):
        """
        Parse datetime from string.

        If there's no template matches your string, Please go
        https://github.com/MacHu-GWU/rolex-project/issues
        submit your datetime string. I 'll update templates ASAP.

        This method is faster than :meth:`dateutil.parser.parse`.

        :param datetime_str: a string represent a datetime
        :type datetime_str: str
        :return: a datetime object

        **中文文档**

        从string解析datetime。首先尝试默认模板, 如果失败了, 则尝试所有的模板。
        一旦尝试成功, 就将当前成功的模板保存为默认模板。这样做在当你待解析的
        字符串非常多, 且模式单一时, 只有第一次尝试耗时较多, 之后就非常快了。
        该方法要快过 :meth:`dateutil.parser.parse` 方法。

        为了防止模板库失败的情况, 程序设定在失败后自动一直启用
        :meth:`dateutil.parser.parse` 进行解析。你可以调用 :meth:`Parser.reset()`
        方法恢复默认设定。
        """
        try:
            a_datetime = datetime.strptime(datetime_str, self._default_datetime_template)
            return a_datetime
        except:
            pass

        for template in datetime_template_list:
            try:
                a_datetime = datetime.strptime(datetime_str, template)
                self._default_datetime_template = template
                return a_datetime
            except:
                pass

        a_datetime = parse(datetime_str)
        self.str2datetime = parse
        return a_datetime

    str2datetime = _str2datetime

    def reset(self):
        """
        Reset :class:`Parser` behavior to default.
        """
        self.str2datetime = self._str2datetime

    def parse_date(self, value):
        """
        A lazy method to parse anything to date.

        If input data type is:

        - string: parse date from it
        - integer: use from ordinal
        - datetime: use date part
        - date: just return it
        """
        if isinstance(value, sixmini.string_types):
            return self.str2date(value)
        if value is None:
            raise TypeError('Unable to parse date from %r' % value)
        else:
            if isinstance(value, sixmini.integer_types):
                return date.fromordinal(value)
            else:
                if isinstance(value, datetime):
                    return value.date()
                if isinstance(value, date):
                    return value
            raise ValueError('Unable to parse date from %r' % value)

    def parse_datetime(self, value):
        """
        A lazy method to parse anything to datetime.

        If input data type is:

        - string: parse datetime from it
        - integer: use from ordinal
        - date: use date part and set hour, minute, second to zero
        - datetime: just return it
        """
        if isinstance(value, sixmini.string_types):
            return self.str2datetime(value)
        if value is None:
            raise TypeError('Unable to parse datetime from %r' % value)
        else:
            if isinstance(value, sixmini.integer_types):
                return from_utctimestamp(value)
            else:
                if isinstance(value, float):
                    return from_utctimestamp(value)
                if isinstance(value, datetime):
                    return value
                if isinstance(value, date):
                    return datetime(value.year, value.month, value.day)
            raise ValueError('Unable to parse datetime from %r' % value)


parser = Parser()