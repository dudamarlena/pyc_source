# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\vis\messager.py
# Compiled at: 2019-12-16 10:38:12
# Size of source mod 2**32: 2131 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
__all__ = [
 'messager']

def print2Terminal(message, type='Normal'):
    """
    Print message to terminal with format, to differentiate errors and warnings

    Args:
        message:    A string for print
        type:       Message type: 'Normal', 'Warning', 'Error'

    Return:
         N/A
    """
    if type != 'Normal':
        if type != 'normal':
            if type != 'NORMAL':
                if type != 'Warning':
                    if type != 'warning':
                        if type != 'WARNING':
                            if type != 'Error':
                                if type != 'error':
                                    if type != 'ERROR':
                                        type = 'normal'
    if type == 'normal' or type == 'Normal' or type == 'NORMAL':
        print('\x1b[0;0;0m' + message)
    if type == 'Warning' or type == 'warning' or type == 'WARNING':
        print('\x1b[1;34;40m' + message)
    if type == 'Error' or type == 'error' or type == 'ERROR':
        print('\x1b[1;31;40m' + message)
    print('\x1b[0;0;0m', end='\r')


class messager:
    print = print2Terminal