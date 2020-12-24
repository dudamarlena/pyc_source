# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/squad_client/exceptions.py
# Compiled at: 2020-02-22 16:49:57
# Size of source mod 2**32: 144 bytes


class InvalidSquadObject(Exception):
    pass


class InvalidReportOutput(Exception):
    pass


class InvalidReportTemplate(Exception):
    pass