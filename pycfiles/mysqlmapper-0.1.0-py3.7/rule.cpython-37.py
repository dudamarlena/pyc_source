# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\verification\rule.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 3256 bytes
import datetime, re

class Rule:
    __doc__ = '\n    Validation rule abstract class\n    '

    def know(self, expr):
        """
        Identification verification rules
        :param expr: Rule expression
        :return: Boer
        """
        pass

    def check(self, dic, expr, name, value):
        """
        Verify expression and corresponding value
        :param dic: Original dictionary
        :param expr: Rule expression
        :param name: Parameter name
        :param value: Value to be verified
        :return: Verification results
        """
        pass


class Required(Rule):

    def know(self, expr):
        return 'required' == expr

    def check(self, dic, expr, name, value):
        b = isinstance(value, str)
        if not b:
            return (
             b, name + ' error in type')
        else:
            b = value != ''
            return b or (
             b, name + ' Field cannot be empty')
        return (
         b, 'success')


class Length(Rule):
    expr = 'length'

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        b = isinstance(value, str)
        if not b:
            return (
             b, name + ' error in type')
        l = len(value)
        minmax = expr[len(self.expr) + 1:len(expr) - 1].split('-')
        min = int(minmax[0])
        max = int(minmax[1])
        if l < min or l > max:
            return (
             False, name + ' Illegal field length')
        return (True, 'success')


class Range(Rule):
    expr = 'range'

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        try:
            value = int(value)
            dic[name] = value
        except Exception as e:
            try:
                print(e)
                return (False, name + ' error in type')
            finally:
                e = None
                del e

        minmax = expr[len(self.expr) + 1:len(expr) - 1].split('-')
        min = int(minmax[0])
        max = int(minmax[1])
        if value < min or value > max:
            return (
             False, name + ' Illegal field range')
        return (True, 'success')


class DateTime(Rule):
    expr = 'datetime'

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        try:
            value = datetime.datetime.strptime(value, pattern)
            dic[name] = value
        except Exception as e:
            try:
                print(e)
                return (False, name + ' error in type')
            finally:
                e = None
                del e

        return (True, 'success')


class Regexp(Rule):
    expr = 'regexp'

    def know(self, expr):
        return expr.startswith(self.expr)

    def check(self, dic, expr, name, value):
        pattern = expr[len(self.expr) + 1:len(expr) - 1]
        search = re.search(pattern, value)
        if search is None:
            return (
             False, name + ' Illegal field format')
        start_end = search.span()
        if start_end[1] - start_end[0] != len(value):
            return (
             False, name + ' Illegal field format')
        return (True, 'success')