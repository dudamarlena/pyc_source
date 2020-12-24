# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/djbaldey/src/sphinx-rosix-theme/rosixdocs/testmodule.py
# Compiled at: 2015-04-22 10:10:34


class AbstractClass(object):
    """
    Использование класса::

        a = AbstractClass()

        print a.test()

    """
    attr = 'атрибут класса'

    def test(self, s='test class'):
        u"""
        Метод печатает строку на стандартный вывод.
        """
        print s

    @property
    def field(self):
        u"""
        Возвращает свойство экземпляра.
        """
        print self.attr


def testfunc(s='test func'):
    u"""
    Функция печатает строку на стандартный вывод.
    """
    print s