# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/md_translate/files_worker.py
# Compiled at: 2019-05-16 02:18:44
# Size of source mod 2**32: 1485 bytes
from pathlib import Path
from typing import Sequence
from md_translate.arguments_processor import ArgumentsProcessor
from md_translate.exceptions import ObjectNotFoundException, FileIsNotMarkdown

class FilesWorker:

    def __init__(self, settings: ArgumentsProcessor):
        self.settings = settings
        self.single_file = False
        self.object_to_process = self.settings.path
        self._FilesWorker__check_for_single_obj()
        self._FilesWorker__validate_folder()
        self.md_files_list = self._FilesWorker__get_md_files_list()

    def __check_for_single_obj(self) -> None:
        if self.object_to_process.is_file():
            if self.object_to_process.suffix == '.md':
                self.single_file = True
        if self.object_to_process.is_file():
            raise FileIsNotMarkdown(self.object_to_process)

    def __validate_folder(self) -> None:
        if not self.object_to_process.exists():
            raise ObjectNotFoundException(self.object_to_process)

    def __get_md_files_list(self) -> Sequence[Path]:
        md_files_list = []
        if self.single_file:
            md_files_list.append(self.object_to_process)
        else:
            for link in self.object_to_process.iterdir():
                if link.suffix == '.md':
                    md_files_list.append(link)

        if len(md_files_list) == 0:
            raise FileNotFoundError('There are no MD files found with provided path!')
        return md_files_list