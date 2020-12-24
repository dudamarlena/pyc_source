# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/md_translate/line_processor.py
# Compiled at: 2019-05-16 02:18:44
# Size of source mod 2**32: 1060 bytes
import re

class LineProcessor:
    code_mark: str = '```'

    def __init__(self, settings, line: str):
        self.settings = settings
        self._line = line
        self.pattern = self.get_regexp(self.settings.source_lang)

    def is_code_block_border(self):
        if self._line == self.code_mark:
            return True
        else:
            return self._line.startswith(self.code_mark) and not self._line.endswith(self.code_mark)

    def line_can_be_translated(self):
        return not self._LineProcessor__is_single_code_line() and self._LineProcessor__is_untranslated_paragraph()

    def __is_untranslated_paragraph(self):
        return re.match(self.pattern, self._line) is not None

    def __is_single_code_line(self):
        return self._line.startswith(self.code_mark) and self._line.endswith(self.code_mark) and len(self._line) > 3

    @staticmethod
    def get_regexp(source_lang=''):
        if source_lang == 'ru':
            return '^[а-яА-Я]+.*'
        else:
            if source_lang == 'en':
                return '^[a-zA-Z]+.*'
            return '^\\d+.*'