# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/document_parsers.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 589 bytes
from pathlib import Path
from exactly_lib.section_document import model
from exactly_lib.section_document.document_parser import DocumentParser
from exactly_lib.section_document.section_parsing import SectionsConfiguration
from .impl import document_parser as _impl

def new_parser_for(configuration: SectionsConfiguration) -> DocumentParser:
    return _impl.DocumentParserForSectionsConfiguration(configuration)


def parse(configuration: SectionsConfiguration, source_file_path: Path) -> model.Document:
    return new_parser_for(configuration).parse_file(source_file_path)