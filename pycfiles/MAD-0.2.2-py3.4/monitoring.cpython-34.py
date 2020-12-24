# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\monitoring.py
# Compiled at: 2016-04-11 03:16:53
# Size of source mod 2**32: 1517 bytes


class CSVReport:
    __doc__ = '\n    Format monitored data as CSV entries and push them in the designated\n    output stream.\n    '

    def __init__(self, output, fields_format):
        self.output = output
        self.formats = fields_format
        self._print_headers()

    def _print_headers(self):
        field_names = [each_key.replace('_', ' ') for each_key, _ in self.formats]
        self.output.write(', '.join(field_names))
        self.output.write('\n')

    def __call__(self, *args, **kwargs):
        texts = []
        for field_name, format in self.formats:
            if field_name in kwargs:
                texts.append(format % kwargs[field_name])
            else:
                texts.append('??')

        self.output.write(', '.join(texts))
        self.output.write('\n')