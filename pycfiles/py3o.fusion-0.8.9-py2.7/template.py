# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/template.py
# Compiled at: 2014-09-10 17:30:38
from twisted.web.template import XMLFile
from twisted.python.filepath import FilePath
import pkg_resources

def tloader(basefile):
    return XMLFile(FilePath(pkg_resources.resource_filename('py3o.fusion', 'templates/%s' % basefile)))