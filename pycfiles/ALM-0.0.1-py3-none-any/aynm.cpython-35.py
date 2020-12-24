# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/AYNM/aynm.py
# Compiled at: 2019-06-13 02:57:14
# Size of source mod 2**32: 2293 bytes
import webbrowser, tkinter as tk

class calc:
    """calc"""

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
    """www"""

    def visit(url):
        """Opens the url in your standard webbrowser"""
        webbrowser.open(url)


class buggie:
    """buggie"""

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
    """og"""

    def og():
        """Some sort of hello world command"""
        print('hello world')


class classes:
    """classes"""
    pass