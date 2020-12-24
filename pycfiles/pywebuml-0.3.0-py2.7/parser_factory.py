# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\parsers\parser_factory.py
# Compiled at: 2011-03-24 10:19:22
""" Gets the parser by the extension of the file.
"""
from pywebuml.parsers.csharp.file_parser import CSharpFileParser
from pywebuml.parsers.java.file_parser import JavaFileParser

def get_parser(file_extension):
    """ Given a file extension, returns the parser for the file.

    :parameters:
        file_extension: str
            the extension of the file that is being parsed.

    :returns:
        the `pywebuml.parsers.FileParser` that will be used for
        that file.
    """
    if file_extension == 'cs':
        return CSharpFileParser()
    if file_extension == 'java':
        return JavaFileParser()