# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/md_translate/file_translator.py
# Compiled at: 2019-05-16 02:18:44
# Size of source mod 2**32: 2169 bytes
import pathlib, re
from typing import Type, Union, IO
from md_translate.arguments_processor import ArgumentsProcessor
from md_translate.line_processor import LineProcessor
from md_translate.translator import get_translator_by_name, AbstractTranslator

class FileTranslator:
    default_open_mode: str = 'r+'
    code_mark: str = '```'
    paragraph_regexp = re.compile('^[a-zA-Z]+.*')

    def __init__(self, settings: ArgumentsProcessor, file_path: pathlib.Path):
        translator_class = get_translator_by_name(settings.service)
        self.settings = settings
        self._FileTranslator__translator = translator_class(settings)
        self._FileTranslator__file_path = file_path
        self.line_processor = None
        self.file_contents_with_translation = []
        self.code_block = False

    def __enter__(self):
        self._FileTranslator__translating_file = self._FileTranslator__file_path.open(self.default_open_mode)
        return self

    def __exit__(self, *args, **kwargs):
        self._FileTranslator__translating_file.close()

    def translate(self):
        lines = self._FileTranslator__translating_file.readlines()
        for counter, line in enumerate(lines):
            self.file_contents_with_translation.append(line)
            self.line_processor = LineProcessor(self.settings, line)
            self.code_block = not self.code_block if self.line_processor.is_code_block_border() else self.code_block
            if self.line_processor.line_can_be_translated() and not self.code_block:
                translated = self._FileTranslator__translator.request_translation(line)
                self.file_contents_with_translation.append('\n')
                if line.endswith('\n'):
                    if not translated.endswith('\n'):
                        self.file_contents_with_translation.append(''.join([translated, '\n']))
                self.file_contents_with_translation.append(translated)

        self._FileTranslator__write_translated_data_to_file()

    def __write_translated_data_to_file(self):
        self._FileTranslator__translating_file.seek(0)
        self._FileTranslator__translating_file.writelines(self.file_contents_with_translation)