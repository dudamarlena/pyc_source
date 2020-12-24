# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/browser/namespace.py
# Compiled at: 2012-06-20 11:31:01
from zope.app.file.interfaces import IFile
from zope.traversing.interfaces import TraversalError
from ztfy.file.interfaces import IImageDisplay
from zope.traversing import namespace

class FilePropertyTraverser(namespace.attr):
    """Simple file property traverser"""

    def traverse(self, name, ignored):
        if '.' in name:
            name = name.split('.', 1)[0]
        result = getattr(self.context, name)
        if not IFile.providedBy(result):
            raise TraversalError('++file++%s' % name)
        return result


class DisplayPropertyTraverser(namespace.attr):
    """Image display property traverser"""

    def traverse(self, name, ignored):
        display = IImageDisplay(self.context, None)
        if display is None:
            raise TraversalError('++display++%s' % name)
        if '.' in name:
            name, format = name.split('.', 1)
        else:
            format = None
        return display.getDisplay(name, format)