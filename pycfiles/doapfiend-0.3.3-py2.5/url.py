# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/url.py
# Compiled at: 2008-05-26 01:02:49
"""

url.py
======

This plugin loads DOAP by its URL or path to a filename.

"""
__docformat__ = 'epytext'
from doapfiend.plugins.base import Plugin
from doapfiend.utils import NotFoundError
from doapfiend.doaplib import fetch_doap

class UrlPlugin(Plugin):
    """Class for formatting DOAP output"""
    name = 'url'
    enabled = False
    enable_opt = name

    def __init__(self):
        """Setup RDF/XML OutputPlugin class"""
        super(UrlPlugin, self).__init__()
        self.options = None
        return

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        search.add_option('-u', '--%s' % self.name, action='store', dest=self.enable_opt, help='Get DOAP by its URL or by filename.', metavar='URL')
        return (parser, output, search)

    def search(self):
        """
        Get DOAP by its URL or file path
        This can be any RDF as long as it has the DOAP namespace.

        @rtype: unicode
        @return: DOAP
        """
        try:
            return fetch_doap(self.options.url, self.options.proxy)
        except NotFoundError:
            print 'Not found: %s' % self.options.url