# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\test.py
# Compiled at: 2019-12-11 15:31:47
# Size of source mod 2**32: 1173 bytes


class X:

    def __init__(self, value):
        self.value = value
        self.__doc_value__ = 'this is an example' + self.value


class A(float):

    def __init__(self, value):
        self.value = value
        self.__doc_value__ = 'this is an example'

    def __repr__(self):
        return 2 * self.value

    def __add__(self, plus):
        return 2 * self.value + plus

    def __abs__(self):
        return 2 * self.value

    def __eq__(self, value):
        if self.value <= 4:
            return not self.value == value
        else:
            return self.value == value

    def __str__(self):
        return '2*' + str(self.value)

    def __rmul__(self, value):
        return self.value / value

    def __radd__(self, value):
        return self.value * 2 + value


class SuperType(int, float, dict, list):

    def __init__(self, value):
        self.value = value


a1 = A(1)
a3 = A(3)
a5 = A(5)
a7 = A(7)
print('1: {}\n3: {}\n5: {}\x07: {}\n'.format(a1, a3, a5, a7))
a4 = a1 + a3
print('1+3=4')
print('{}+{}={}\n'.format(a1, a3, a4))
print('4==5')
print(a4 == a5)