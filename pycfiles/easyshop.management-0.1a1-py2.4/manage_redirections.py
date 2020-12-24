# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/management/browser/manage_redirections.py
# Compiled at: 2008-09-01 03:10:27
import re
from zope.component import getUtility
from Products.CMFPlone import Batch
from Products.Five.browser import BrowserView
from plone.app.redirector.interfaces import IRedirectionStorage

class ManageRedirectionsView(BrowserView):
    """
    """
    __module__ = __name__

    def getRedirections(self):
        """Returns all stored redirections.
        """
        storage = getUtility(IRedirectionStorage)
        result = []
        for (old_path, new_path) in storage._paths.items():
            result.append({'old_path': old_path, 'new_path': new_path})

        b_start = self.request.get('b_start', 0)
        amount = self.request.get('amount', 20)
        return Batch(result, int(amount), int(b_start), orphan=0)

    def addRedirection(self):
        """
        """
        old_path = self.request.get('old_path', '')
        new_path = self.request.get('new_path', '')
        if old_path != '' and new_path != '':
            storage = getUtility(IRedirectionStorage)
            storage.add(old_path, new_path)
        self._redirect()

    def cleanupRedirections(self):
        """
        """
        storage = getUtility(IRedirectionStorage)
        to_delete_paths = []
        for (key, value) in storage._paths.items():
            if key == value:
                to_delete_paths.append(key)

        for path in to_delete_paths:
            storage.remove(path)

        self._redirect()

    def removeRedirection(self):
        """Removes given path
        """
        path = self.request.get('path', '')
        if path != '' and storage.has_path(path):
            storage = getUtility(IRedirectionStorage)
            storage.remove(path)
        self._redirect()

    def removeRedirections(self):
        """
        """
        paths = self.request.get('paths', [])
        if not isinstance(paths, (list, tuple)):
            paths = (
             paths,)
        storage = getUtility(IRedirectionStorage)
        for path in paths:
            if path != '' and storage.has_path(path):
                storage.remove(path)

        regex = self.request.get('regex', '')
        if regex != '':
            to_delete_paths = []
            for path in storage._paths.keys():
                if re.search(regex, path):
                    to_delete_paths.append(path)

            for path in to_delete_paths:
                storage.remove(path)

        self._redirect()

    def _redirect(self):
        """
        """
        amount = self.request.get('amount', '')
        b_start = self.request.get('b_start', '')
        if amount == '':
            amount = 0
        if b_start == '':
            b_start = 0
        url = self.context.absolute_url() + '/manage-redirections?b_start:int=' + str(b_start) + '&amount=' + amount
        self.request.response.redirect(url)