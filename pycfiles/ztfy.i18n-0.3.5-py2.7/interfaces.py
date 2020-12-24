# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/tal/interfaces.py
# Compiled at: 2012-06-20 11:46:34
from zope.interface import Interface

class II18nTalesAPI(Interface):

    def __getattr__(attribute):
        """Extract translated or default value of the given attribute"""
        pass

    def translate():
        """Translate context according to current request"""
        pass

    def langs():
        """Get list of langs available in the current context, default one being first"""
        pass

    def user_lang():
        """Get current user preferred language"""
        pass

    def default_lang():
        """Get current default lang"""
        pass