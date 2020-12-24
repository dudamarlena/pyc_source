# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Servlet.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = "\nProvides an abstract Servlet baseclass for Cheetah's Template class\n"
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