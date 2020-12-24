# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcel/workspace/python-ipagare/ipagare/error.py
# Compiled at: 2012-10-04 15:00:59


class IPagareError(Exception):

    def __init__(self, error):
        self.code = error.get('codigo').encode('utf-8')
        self.description = error.get('descricao').encode('utf-8')
        error_text = ('IPagare Error {}: {}').format(self.code, self.description)
        super(IPagareError, self).__init__(error_text)