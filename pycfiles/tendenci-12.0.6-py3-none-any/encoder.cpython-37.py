# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/wp_exporter/encoder.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 842 bytes
from builtins import str

class XML:

    def __init__(self, version='1.0', encoding='UTF-8'):
        self.content = '<?xml version="%s" encoding="%s"?>\n' % (version, encoding)

    def write(self, text, depth=0):
        txt = ''
        for i in range(0, depth):
            txt += '    '

        txt += str(text) + '\n'
        self.content += txt

    def open(self, name, attrs={}, depth=0):
        txt = ''
        for i in range(0, depth):
            txt += '    '

        self.content += txt
        self.content += '<%s' % name
        for key in attrs:
            self.content += ' %s = "%s"' % (key, attrs[key])

        self.content += '>\n'

    def close(self, name, depth=0):
        txt = ''
        for i in range(0, depth):
            txt += '    '

        self.content += txt
        self.content += '</%s>\n' % name