# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/freshmeat.py
# Compiled at: 2008-05-21 11:37:15
"""

freshmeat
=========

Currently this plugin uses http://doapspace.org/ to fetch DOAP for Freshmeat

"""
__docformat__ = 'epytext'
from doapfiend.utils import NotFoundError
from doapfiend.plugins.base import Plugin
from doapfiend.plugins.pkg_index import get_by_pkg_index

class FreshmeatPlugin(Plugin):
    """Get DOAP from Freshmeat package index"""
    name = 'fm'
    enabled = False
    enable_opt = name

    def __init__(self):
        """Setup RDF/XML OutputPlugin class"""
        super(FreshmeatPlugin, self).__init__()
        self.options = None
        self.query = None
        return

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        search.add_option('--%s' % self.name, action='store', dest=self.enable_opt, help='Get DOAP by its Freshmeat project name.', metavar='PROJECT_NAME')
        return (parser, output, search)

    def search(self, proxy=None):
        """
        Get Freshmeat DOAP

        @param proxy: URL of optional HTTP proxy
        @type proxy: string

        @rtype: unicode
        @returns: Single DOAP

        """
        if hasattr(self.options, self.name):
            self.query = getattr(self.options, self.name)
        try:
            return get_by_pkg_index(self.name, self.query, proxy)
        except NotFoundError:
            print 'Not found: %s' % self.query