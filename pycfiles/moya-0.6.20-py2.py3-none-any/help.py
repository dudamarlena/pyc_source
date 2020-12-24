# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/elements/help.py
# Compiled at: 2015-09-22 18:01:38
from __future__ import unicode_literals
from __future__ import print_function
from ..console import make_table_header
from ..tools import extract_namespace
from .. import namespaces
from ..console import Cell
from .. import bbcode
import textwrap

def help(archive, console, tagname):
    """Generate console help"""
    xmlns, tagname = extract_namespace(tagname)
    if b'/' not in xmlns:
        xmlns = namespaces.default + b'/' + xmlns
    tag = archive.registry.get_tag((b'{{{}}}{}').format(xmlns, tagname))
    if tag is None:
        if xmlns and not archive.registry.check_namespace(xmlns):
            console.error(b'No such namespace: %s' % xmlns)
        else:
            console.error(b'No such tag: %s' % tagname)
        return False
    tag_name = tag._tag_name
    doc = b'<%s/>' % tag_name
    doc_attribs = []
    for name, attrib in sorted(tag._tag_attributes.items()):
        if attrib.metavar:
            metavar = attrib.metavar.upper()
            doc_attribs.append(b'%s="%s"' % (attrib.name or name, metavar))

    if doc_attribs:
        doc = b'<%s %s />' % (tag_name, (b' ').join(doc_attribs))
    else:
        doc = b'<%s/>' % tag_name
    console.xml(doc.strip()).nl()
    if tag._tag_doc:
        console(bbcode.render_console(tag._tag_doc, max_length=console.width)).nl()
    details = [(Cell(b'name', bold=True), tagname),
     (
      Cell(b'synopsis', bold=True), getattr(tag.Help, b'synopsis', None) if hasattr(tag, b'Help') else b''),
     (
      Cell(b'namespace', bold=True), xmlns),
     (
      Cell(b'defined', bold=True), getattr(tag, b'_definition', b'?'))]
    console.table(details, header=False, dividers=False, grid=False).nl()
    if hasattr(tag, b'Help'):
        example = getattr(tag.Help, b'example', None)
        if example:
            example = textwrap.dedent(example)
            console(b'[example(s)]', fg=b'magenta', bold=True).nl()
            console.xml(example).nl()
    base_attributes = tag._get_base_attributes()
    params = []
    for name, attrib in tag._tag_attributes.items():
        if name not in base_attributes:
            params.append((Cell((b'"{}"').format(name), fg=b'cyan'),
             attrib.doc,
             attrib.type_display.lower(),
             b'Yes' if attrib.required else b'No',
             (attrib.required or attrib.default_display)(attrib.default) if 1 else b''))

    params.sort(key=lambda p: p[0])
    if params:
        console(b'[attributes]', fg=b'green', bold=True).nl()
        console.table(make_table_header(b'attrib', b'doc', b'type', b'required?', b'default') + params).nl()
    params = []
    for name, attrib in base_attributes.items():
        if name in tag._tag_attributes:
            docattrib = tag._tag_attributes[name]
        else:
            docattrib = attrib
        params.append((Cell((b'"{}"').format(name), fg=b'cyan'),
         docattrib.doc,
         docattrib.type_display.lower(),
         b'Yes' if docattrib.required else b'No',
         (docattrib.required or docattrib).default if 1 else b''))

    if params:
        console(b'[inherited attributes]', fg=b'green', bold=True).nl()
        console.table(make_table_header(b'attrib', b'doc', b'type', b'required?', b'default') + params)
    return True