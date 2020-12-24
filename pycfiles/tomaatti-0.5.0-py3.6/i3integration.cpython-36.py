# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/i3integration.py
# Compiled at: 2018-06-19 09:05:36
# Size of source mod 2**32: 1517 bytes


class I3Integration(object):
    CLICKED_BUTTON_ENVIRON = 'BLOCK_BUTTON'
    BLOCK_NAME_ENVIRON = 'BLOCK_NAME'
    BLOCK_INSTANCE_ENVIRON = 'BLOCK_INSTANCE'
    LEFT_MOUSE_BUTTON = 1
    MIDDLE_MOUSE_BUTTON = 2
    RIGHT_MOUSE_BUTTON = 3
    MOUSE_SCROLL_UP = 4
    MOUSE_SCROLL_DOWN = 5

    @staticmethod
    def get_clicked_button() -> int:
        from os import environ
        if I3Integration.CLICKED_BUTTON_ENVIRON in environ:
            try:
                return int(environ[I3Integration.CLICKED_BUTTON_ENVIRON])
            except ValueError:
                return -1

        return -1

    @staticmethod
    def get_block_name() -> str:
        from os import environ
        if I3Integration.BLOCK_NAME_ENVIRON in environ:
            return environ[I3Integration.BLOCK_NAME_ENVIRON]
        else:
            return ''

    @staticmethod
    def get_block_instance() -> str:
        from os import environ
        if I3Integration.BLOCK_INSTANCE_ENVIRON in environ:
            return environ[I3Integration.BLOCK_INSTANCE_ENVIRON]
        else:
            return ''