# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/impl/file_access.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1282 bytes
from pathlib import Path
from typing import Sequence, Optional
from exactly_lib.section_document.exceptions import FileAccessError
from exactly_lib.section_document.impl.utils import new_for_file
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.source_location import SourceLocation

def read_source_file(file_path: Path, file_path_for_error_message: Path, file_inclusion_chain: Sequence[SourceLocation], section_name: Optional[str]=None) -> ParseSource:
    try:
        return new_for_file(file_path)
    except OSError as ex:
        raise FileAccessError(file_path_for_error_message, str(ex), file_inclusion_chain, section_name)


def resolve_path(path: Path, file_inclusion_chain: Sequence[SourceLocation], section_name: Optional[str]=None) -> Path:
    try:
        return path.resolve()
    except RuntimeError as ex:
        raise FileAccessError(path, str(ex), file_inclusion_chain, section_name)