# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/namespace.py
# Compiled at: 2012-06-20 11:46:34
from z3c.language.switch.interfaces import II18n
from zope.traversing.interfaces import TraversalError
from zope.app.file.interfaces import IFile
from zope.traversing import namespace

class I18nFilePropertyTraverser(namespace.view):
    """Simple file property traverser"""

    def traverse(self, name, ignored):
        if '.' in name:
            name = name.split('.', 1)[0]
        if ':' in name:
            name, lang = name.split(':')
            result = II18n(self.context).getAttribute(name, language=lang)
        else:
            result = II18n(self.context).queryAttribute(name, request=self.request)
        if not IFile.providedBy(result):
            raise TraversalError('++i18n++%s' % name)
        return result