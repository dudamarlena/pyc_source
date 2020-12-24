# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/theme/bplus_cms.py
# Compiled at: 2010-04-22 17:25:58
"""
    MoinMoin - bplus_cms theme

    @copyright: 2009 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""
from MoinMoin.theme.modernized import Theme as ThemeBase

class Theme(ThemeBase):
    name = 'bplus'

    def onlyloggedin(method):
        """ decorator that returns empty string for not logged-in users,
            otherwise it calls the decorated method
        """
        return lambda self, *args, **kwargs: self.request.user.valid and self.request.user.name and method(self, *args, **kwargs) or ''

    interwiki = onlyloggedin(ThemeBase.interwiki)
    title = onlyloggedin(ThemeBase.title)
    username = onlyloggedin(ThemeBase.username)
    pageinfo = onlyloggedin(ThemeBase.pageinfo)
    editbar = onlyloggedin(ThemeBase.editbar)


def execute(request):
    return Theme(request)