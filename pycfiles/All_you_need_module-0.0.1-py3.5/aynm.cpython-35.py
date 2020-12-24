# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/AYNM/aynm.py
# Compiled at: 2019-06-13 02:57:14
# Size of source mod 2**32: 2293 bytes
import webbrowser, tkinter as tk

class calc:
    __doc__ = '\n    A maths class that contains a calculator and some other good stuff\n    '

    def prtclc(a, operator, b):
        """
        prtclc stands for print calculator wich is a calculator that prints the answer on the screen
        """
        if operator == '+':
            answr = a + b
        else:
            if operator == '-':
                answr = a - b
            else:
                if operator == '*':
                    answr = a * b
                else:
                    if operator == '/':
                        answr = a / b
                    else:
                        raise ValueError(operator, ' is not  a operator. The operators are + , - , * and / . If you wrote one of those make sure it is a string, not a variable.')
        print(answr)

    def even(number_to_check):
        """
        A function that checks if number_to_check is even and return True or False
        """
        if number_to_check % 2 == 0:
            return True
        else:
            return False

    def odd(number_to_check):
        """
        A function that checks if number_to_check is odd and returns either True or False as an output
        """
        if not number_to_check % 2 == 0:
            return True
        else:
            return False


class www:
    __doc__ = '\n    A class that contains internet functions\n    NEEDS webbrowser module and internet\n    '

    def visit(url):
        """Opens the url in your standard webbrowser"""
        webbrowser.open(url)


class buggie:
    __doc__ = 'A class with functions that goes on forever'

    def zero():
        """Zero Zero Zero... What else do you need to know"""
        while True:
            print('000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    def window():
        """A alpha function that does not work as supposed"""
        while True:
            root = tk.Tk()
            window = tk.Toplevel(root)
            tk.mainloop()


class og:
    __doc__ = "Well, it's the og class"

    def og():
        """Some sort of hello world command"""
        print('hello world')


class classes:
    __doc__ = 'A class made for documentation. The classes in the documentation is Calc , www , buggie , og and classes (a special documentation class)'