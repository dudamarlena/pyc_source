# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/document_parser.py
# Compiled at: 2019-11-15 18:53:47
# Size of source mod 2**32: 2631 bytes
from pathlib import Path
from typing import List
from exactly_lib.section_document import model
from exactly_lib.section_document.impl import file_access as _file_access
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.source_location import FileLocationInfo

class DocumentParser:
    __doc__ = '\n    Base class for parsers that parse a "plain file"\n    (i.e., a file that do not need pre-processing).\n    '

    def parse_file(self, source_file_path: Path) -> model.Document:
        """
        :raises ParseError The test case cannot be parsed.
        """
        source = _file_access.read_source_file(source_file_path, source_file_path, [])
        return self.parse_source(source_file_path, source)

    def parse_source(self, source_file_path: Path, source: ParseSource) -> model.Document:
        """
        :param source_file_path: None iff the source is not a file - e.g. stdin.
        :param source: The source to parse - the contents of source_file_path, if the source is from a file.
        :raises ParseError The test case cannot be parsed.
        """
        file_location_info = self._resolve_initial_file_location_info(source_file_path)
        return self._parse(file_location_info.abs_path_of_dir_containing_last_file_base_name, file_location_info, [
         source_file_path.resolve()], source)

    def _parse(self, file_reference_relativity_root_dir: Path, file_location_info: FileLocationInfo, visited_paths: List[Path], source: ParseSource) -> model.Document:
        """
        :param file_reference_relativity_root_dir: A directory that file reference paths are relative to.
        :param source: The source to parse - the contents of source_file_path, if the source is from a file.
        :raises ParseError The test case cannot be parsed.
        """
        raise NotImplementedError('abstract method')

    @staticmethod
    def _resolve_initial_file_location_info(source_file_path: Path) -> FileLocationInfo:
        abs_path_of_dir_containing_first_file_path = Path('/') if source_file_path.is_absolute() else _file_access.resolve_path(Path.cwd(), [])
        return FileLocationInfo(abs_path_of_dir_containing_first_file_path, source_file_path, [])