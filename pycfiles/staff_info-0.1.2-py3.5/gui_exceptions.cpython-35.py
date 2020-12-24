# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staff_info/gui_exceptions.py
# Compiled at: 2018-05-08 08:44:40
# Size of source mod 2**32: 270 bytes


class GUIException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TooManyItemsChecked(GUIException):

    def __init__(self, *args):
        super().__init__('Expected 1 argument, received {}'.format(len(args)))