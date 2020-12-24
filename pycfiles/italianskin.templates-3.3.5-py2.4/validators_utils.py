# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/italianskin/templates/validators_utils.py
# Compiled at: 2010-09-08 03:48:21
from zope.interface import implements
from Products.Five.browser import BrowserView
from italianskin.templates.interfaces import IValidatorView
from italianskin.templates.config import VALIDATOR_URL

class ValidatorView(BrowserView):
    """ """
    __module__ = __name__
    implements(IValidatorView)

    def validateURL(self):
        return VALIDATOR_URL % {'URL': self.context.absolute_url()}