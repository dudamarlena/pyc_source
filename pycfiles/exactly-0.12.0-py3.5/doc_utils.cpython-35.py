# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/render/doc_utils.py
# Compiled at: 2017-12-07 08:04:08
# Size of source mod 2**32: 591 bytes
from exactly_lib.util.textformat.structure import document as doc
from exactly_lib.util.textformat.structure import structures as docs

def synopsis_section(contents: doc.SectionContents) -> doc.Section:
    return doc.Section(docs.text('SYNOPSIS'), contents)


def description_section(contents: doc.SectionContents) -> doc.Section:
    return doc.Section(docs.text('DESCRIPTION'), contents)


def description_section_if_non_empty(contents: doc.SectionContents) -> list:
    if contents.is_empty:
        return []
    else:
        return [
         doc.Section(docs.text('DESCRIPTION'), contents)]