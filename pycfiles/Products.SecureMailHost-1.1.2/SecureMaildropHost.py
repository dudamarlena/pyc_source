# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/Products/SecureMaildropHost/SecureMaildropHost.py
# Compiled at: 2007-08-04 12:34:10
from Globals import DTMLFile
from Products.SecureMailHost.SecureMailHost import SecureMailHost
from Products.MaildropHost import MaildropHost
addSecureMaildropHostForm = DTMLFile('www/addSecureMaildropHost_form', globals())

def manage_addSecureMaildropHost(self, id, title='', REQUEST=None):
    """add a SecureMaildropHost"""
    smdh = SecureMaildropHost(id, title)
    self._setObject(id, smdh)
    if REQUEST is not None:
        ret_url = '%s/%s/manage_main' % (self.absolute_url(), id)
        REQUEST['RESPONSE'].redirect(ret_url)
    return


class SecureMaildropHost(MaildropHost, SecureMailHost):
    __module__ = __name__
    meta_type = 'Secure Maildrop Host'

    def _send(self, mfrom, mto, messageText, debug=False):
        """Send a mail using the asynchronous maildrop handler"""
        if hasattr(messageText, 'as_string'):
            msg = messageText.as_string()
        else:
            msg = str(messageText)
        MaildropHost._send(self, mfrom, mto, msg)