# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/error.py
# Compiled at: 2010-07-12 01:59:01
"""Exceptions and Errors"""

class ZetaError(Exception):
    """Exception base class for errors in Zeta."""
    title = 'Zeta Error'

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    def __init__(self, message, title=None, show_traceback=False):
        Exception.__init__(self, message)
        self.message = message
        if title:
            self.title = title
        self.show_traceback = show_traceback

    def __unicode__(self):
        return unicode(self.message)

    message = property(_get_message, _set_message)


class ZetaComponentError(ZetaError):
    """Handles all errors detected on Component core"""
    pass


class ZetaPermError(ZetaError):
    """Handles all errors detected on user / project permissions"""
    pass


class ZetaUserError(ZetaError):
    """Use this exception to raise errors related to user auth component and
    models."""
    pass


class ZetaAuthorizationError(ZetaError):
    """Handles all errors detected on user information"""
    pass


class ZetaAuthenticationError(ZetaError):
    """Handles all errors detected on user information"""
    pass


class ZetaTagError(ZetaError):
    """Use this exception to raise errors related to Tag component and
    models."""
    pass


class ZetaAttachError(ZetaError):
    """Use this exception to raise errors related to Attachment component and
    models."""
    pass


class ZetaLicenseError(ZetaError):
    """Use this exception to raise errors related to License component and
    models."""
    pass


class ZetaProjectError(ZetaError):
    """Use this exception to raise errors related to Project component and
    models."""
    pass


class ZetaTicketError(ZetaError):
    """Use this exception to raise errors related to Ticket component and
    models."""
    pass


class ZetaWikiError(ZetaError):
    """Use this exception to raise errors related to Wiki component and
    models."""
    pass


class ZetaFormError(ZetaError):
    """Handles all errors detected during form request/submit"""
    pass


class ZetaSMTPError(ZetaError):
    """Handles all smtp client error"""
    pass


class ZetaPOP3Error(ZetaError):
    """Handles all pop3 client error"""
    pass


class ZetaMailtextParse(ZetaError):
    """Handles all mail text parse error"""
    pass