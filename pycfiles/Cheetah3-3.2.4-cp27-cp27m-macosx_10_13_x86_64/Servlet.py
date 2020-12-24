# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Servlet.py
# Compiled at: 2019-09-22 10:12:27
"""
Provides an abstract Servlet baseclass for Cheetah's Template class
"""
import os.path

class Servlet(object):
    """
        This class is an abstract baseclass for Cheetah.Template.Template.
    """
    transaction = None
    application = None
    request = None
    session = None

    def respond(self, trans=None):
        raise NotImplementedError("couldn't find the template's main method.  If you are using #extends\nwithout #implements, try adding '#implements respond' to your template\ndefinition.")

    def sleep(self, transaction):
        super(Servlet, self).sleep(transaction)
        self.session = None
        self.request = None
        self._request = None
        self.response = None
        self.transaction = None
        return

    def shutdown(self):
        pass

    def serverSidePath(self, path=None, normpath=os.path.normpath, abspath=os.path.abspath):
        if path:
            return normpath(abspath(path.replace('\\', '/')))
        else:
            if hasattr(self, '_filePath') and self._filePath:
                return normpath(abspath(self._filePath))
            else:
                return

            return