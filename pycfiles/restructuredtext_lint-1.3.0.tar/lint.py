# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/todd/github/restructuredtext-lint/restructuredtext_lint/lint.py
# Compiled at: 2018-11-14 00:55:13
from __future__ import absolute_import
import io
from docutils import utils
from docutils.core import Publisher
from docutils.nodes import Element

def lint(content, filepath=None, rst_prolog=None):
    """Lint reStructuredText and return errors

    :param string content: reStructuredText to be linted
    :param string filepath: Optional path to file, this will be returned as the source
    :param string rst_prolog: Optional content to prepend to content, line numbers will be offset to ignore this
    :rtype list: List of errors. Each error will contain a line, source (filepath),
        message (error message), and full message (error message + source lines)
    """
    pub = Publisher(None, None, None, settings=None)
    pub.set_components('standalone', 'restructuredtext', 'pseudoxml')
    settings = pub.get_settings(halt_level=5)
    pub.set_io()
    reader = pub.reader
    document = utils.new_document(filepath, settings)
    document.reporter.stream = None
    errors = []
    rst_prolog_line_offset = 0
    if rst_prolog:
        content = rst_prolog + '\n' + content
        rst_prolog_line_offset = rst_prolog.count('\n') + 1

    def error_collector(data):
        data.line = data.get('line')
        if isinstance(data.line, int):
            data.line -= rst_prolog_line_offset
        data.source = data['source']
        data.level = data['level']
        data.type = data['type']
        data.message = Element.astext(data.children[0])
        data.full_message = Element.astext(data)
        errors.append(data)

    document.reporter.attach_observer(error_collector)
    reader.parser.parse(content, document)
    document.transformer.populate_from_components((
     pub.source, pub.reader, pub.reader.parser, pub.writer, pub.destination))
    transformer = document.transformer
    while transformer.transforms:
        if not transformer.sorted:
            transformer.transforms.sort()
            transformer.transforms.reverse()
            transformer.sorted = 1
        priority, transform_class, pending, kwargs = transformer.transforms.pop()
        transform = transform_class(transformer.document, startnode=pending)
        transform.apply(**kwargs)
        transformer.applied.append((priority, transform_class, pending, kwargs))

    return errors


def lint_file(filepath, encoding=None, *args, **kwargs):
    """Lint a specific file"""
    with io.open(filepath, encoding=encoding) as (f):
        content = f.read()
    return lint(content, filepath, *args, **kwargs)