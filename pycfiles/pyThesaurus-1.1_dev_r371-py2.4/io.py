# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/io.py
# Compiled at: 2008-10-06 10:31:21
import dircache, re, pyThesaurus
from imp import find_module, load_module
from pyThesaurus.Thesaurus import Thesaurus
from StringIO import StringIO

def registerFormat(filetype, filehandler):
    _formats[filetype] = filehandler


def read(input, format, default_language, default_contexts=[], thesaurus=Thesaurus()):
    if format not in _formats:
        raise Exception, 'Format %s not supported' % format
    if isinstance(input, str):
        input = StringIO(input)
    io = _formats[format](default_language, contexts=default_contexts, thesaurus=thesaurus)
    io.read(input)


def write(output, format, languages, contexts=[]):
    if format not in _formats:
        raise Exception, 'Format %s not supported' % format
    if isinstance(input, str):
        output = StringIO(output)
    io = _formats[format](default_language, thesaurus=thesaurus, contexts=default_contexts)
    io.write(output)


def formats():
    return _formats.keys()


_formats = {}
import ioDing, ioSKOSCore