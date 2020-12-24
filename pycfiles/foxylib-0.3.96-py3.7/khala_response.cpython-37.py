# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/khalalib/response/khala_response.py
# Compiled at: 2019-10-13 17:45:56
# Size of source mod 2**32: 305 bytes


class KhalaResponse:

    class Field:
        TEXT = 'text'

    F = Field

    class Builder:

        @classmethod
        def str2j_response(cls, str_out):
            return {KhalaResponse.F.TEXT: str_out}

    @classmethod
    def j_response2text(cls, j_response):
        return j_response[cls.F.TEXT]