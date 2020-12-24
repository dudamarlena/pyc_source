# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/template.py
# Compiled at: 2014-09-10 17:30:38
from twisted.web.template import XMLFile
from twisted.python.filepath import FilePath
import pkg_resources

def tloader(basefile):
    return XMLFile(FilePath(pkg_resources.resource_filename('py3o.fusion', 'templates/%s' % basefile)))