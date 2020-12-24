# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/element_parsers/source_utils.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1009 bytes
from contextlib import contextmanager
from exactly_lib.section_document.element_parsers.misc_utils import new_token_stream
from exactly_lib.section_document.parse_source import ParseSource

@contextmanager
def token_stream_from_parse_source(parse_source: ParseSource):
    """
    Gives a :class:`TokenStream` backed by the given :class:`ParseSource`.

    The source of the :class:`TokenStream` is the remaining sources of the :class:`ParseSource`
    """
    ts = new_token_stream(parse_source.remaining_source)
    yield ts
    parse_source.consume(ts.position)


@contextmanager
def token_stream_from_remaining_part_of_current_line_of_parse_source(parse_source: ParseSource):
    """
    Gives a :class:`TokenStream` backed by the given :class:`ParseSource`.

    The source of the :class:`TokenStream` is the remaining part of the current line of the :class:`ParseSource`
    """
    ts = new_token_stream(parse_source.remaining_part_of_current_line)
    yield ts
    parse_source.consume(ts.position)