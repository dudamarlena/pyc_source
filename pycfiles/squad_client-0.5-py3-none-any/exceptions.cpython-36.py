# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/exceptions.py
# Compiled at: 2020-04-08 08:25:25
# Size of source mod 2**32: 146 bytes


class InvalidSquadObject(Exception):
    pass


class InvalidReportOutput(Exception):
    pass


class InvalidReportTemplate(Exception):
    pass