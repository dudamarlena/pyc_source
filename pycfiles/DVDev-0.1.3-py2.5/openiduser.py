# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/controllers/openiduser.py
# Compiled at: 2009-04-17 21:13:48
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from dvdev.lib.base import BaseController, render
from pylons import config
from os import path, makedirs
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter
from mercurial import commands, ui, hg
from re import compile
log = logging.getLogger(__name__)

class OpeniduserController(BaseController):

    def login(self):
        return render('login.html')

    def success(self):
        output = ''
        for (repo, root) in self.repositories:
            self.ui.pushbuffer()
            commands.diff(self.ui, repo)
            output += self.ui.popbuffer()

        css = '<style type="text/css">%s</style>' % HtmlFormatter().get_style_defs('.highlight')
        return self.workspace
        return '%s User: %s' % (css, highlight(output, DiffLexer(), HtmlFormatter()))