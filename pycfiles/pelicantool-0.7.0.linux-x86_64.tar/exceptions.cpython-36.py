# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cufrancis/Develop/pelicantool/.env/lib/python3.6/site-packages/pelicantool/exceptions.py
# Compiled at: 2018-01-12 20:57:48
# Size of source mod 2**32: 134 bytes


class ParserNotFound(Exception):
    pass


class ActionNotFound(Exception):
    pass


class InterfaceNotImplete(Exception):
    pass