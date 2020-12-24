# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/secure.py
# Compiled at: 2010-05-21 08:57:50
__doc__ = 'Sample controller with all its actions protected.'
from tg import expose, flash
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from pyf.services.lib.base import BaseController
__all__ = [
 'SecureController']

class SecureController(BaseController):
    """Sample controller-wide authorization"""
    allow_only = has_permission('manage', msg=l_('Only for people with the "manage" permission'))

    @expose('pyf.services.templates.index')
    def index(self):
        """Let the user know that's visiting a protected controller."""
        flash(_('Secure Controller here'))
        return dict(page='index')

    @expose('pyf.services.templates.index')
    def some_where(self):
        """Let the user know that this action is protected too."""
        return dict(page='some_where')