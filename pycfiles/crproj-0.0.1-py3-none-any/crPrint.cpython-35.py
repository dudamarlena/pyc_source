# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv7l/egg/crPrint.py
# Compiled at: 2017-01-14 03:13:42
# Size of source mod 2**32: 842 bytes
__doc__ = " \n    Exemplo:\n    --------\n\n        >>> from crPrint import cprint\n        >>>  cprint('OLA MUNDO','Green')\n        OLA MUNDO\n\n   © Copyright 2017 João Mário\n\n"
__author__ = 'João Mário'
__mail__ = 'joaok63@outlook.com'
__copyright__ = '© 2017 João Mário'
__license__ = 'GPL'

def cprint(texto='', cor=''):
    if cor == 'Red':
        print('\x1b[91m%s\x1b[0m' % texto)
    else:
        if cor == 'Yellow':
            print('\x1b[93m%s\x1b[0m' % texto)
        else:
            if cor == 'Green':
                print('\x1b[92m%s\x1b[0m' % texto)
            else:
                if cor == 'Pink':
                    print('\x1b[95m%s\x1b[0m' % texto)
                else:
                    if cor == 'Blue':
                        print('\x1b[94m%s\x1b[0m' % texto)
                    else:
                        if cor == 'Cyan':
                            print('\x1b[96m%s\x1b[0m' % texto)
                        else:
                            print(texto)


if __name__ == '__main__':
    exit()