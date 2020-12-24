# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/crPrint.py
# Compiled at: 2017-01-14 03:13:42
# Size of source mod 2**32: 842 bytes
""" 
    Exemplo:
    --------

        >>> from crPrint import cprint
        >>>  cprint('OLA MUNDO','Green')
        OLA MUNDO

   © Copyright 2017 João Mário

"""
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