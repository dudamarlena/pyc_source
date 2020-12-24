# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/phial/documents.py
# Compiled at: 2014-05-21 21:15:20
__all__ = [
 'open_file', 'parse_document', 'Document']
import StringIO, codecs, os, yaml
from . import exceptions

class UnicodeSafeLoader(yaml.SafeLoader):
    """YAML loader that uses unicode rather than str.

    We need to get PyYAML to use the Python unicode object to store any strings
    present in the YAML. Therefore we override the default handling of YAML
    strings here. The default handling will return a str if every character is
    a valid ASCII character.
    """
    yaml_constructors = {'tag:yaml.org,2002:str': lambda loader, node: loader.construct_scalar(node)}


def open_file(path):
    """
    Open a file with the correct decoder according to the
    `YAML 1.1 spec <http://yaml.org/spec/1.1/#id868742>`_, with the notable
    addition of correct handling of the
    `UTF-8 with BOM signature <http://en.wikipedia.org/wiki/Byte_order_mark#UTF-8>`_
    encoding.

    :param path: The location of the file on the operating system. It will be
        opened for reading only.

    :returns: A file-like object as returned by
        `codecs.open() <http://docs.python.org/2/library/codecs.html#codecs.open>`_.

    """
    DEFAULT_ENCODING = 'utf_8'
    BOMS = [
     (
      codecs.BOM_UTF8, 'utf_8_sig'),
     (
      codecs.BOM_UTF16_BE, 'utf_16'),
     (
      codecs.BOM_UTF16_LE, 'utf_16')]
    with open(path, 'rb') as (raw_file):
        max_bom_length = reduce(max, [ len(i[0]) for i in BOMS ])
        front_data = raw_file.read(max_bom_length)
    file_encoding = DEFAULT_ENCODING
    for bom, encoding in BOMS:
        if front_data.startswith(bom):
            file_encoding = encoding
            break

    return codecs.open(path, 'r', encoding=file_encoding)


def parse_document(document_file):
    """
    Will parse a document into its frontmatter and content components. The
    frontmatter will be decoded with a YAML parser.

    :param document_file: A file-like object to consume. It must produce
        ``unicode`` objects when read from rather than ``str``.

    :returns: A two-tuple ``(frontmatter, content)``.

    """
    FRONT_MATTER_END = '...'
    front_matter = StringIO.StringIO()
    for line in document_file:
        assert isinstance(line, unicode)
        front_matter.write(line)
        if line.rstrip() == FRONT_MATTER_END:
            break
    else:
        document_file.seek(0)
        return (None, document_file.read())

    decoded_front_matter = yaml.load(front_matter.getvalue(), UnicodeSafeLoader)
    content = document_file.read()
    while True:
        data = document_file.read()
        if data == '':
            break
        content += data

    return (decoded_front_matter, content)


class Document:
    """
    A Phial document.

    :ivar file_path: If applicable, the path to the document on the filesystem,
        may be ``None``.
    :ivar frontmatter: A dictionary containing the parsed frontmatter of the
        document.
    :ivar content: A unicode string containing the content of the document (which is
        defined as everything that's not the frontmatter).
    """

    def __init__(self, document, file_path=None):
        """
        :param document: May be either a path or a file-like object.

        """
        if isinstance(document, basestring):
            self.file_path = os.path.abspath(document)
            document_file = open_file(document)
        else:
            self.file_path = None
            document_file = document
        self.frontmatter, self.content = parse_document(document_file)
        return