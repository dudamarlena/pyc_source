# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend/plugins/homepage.py
# Compiled at: 2008-05-26 02:11:05
"""

homepage
========

Fetches DOAP by searching doapspace.org by a project's homepage.

"""
__docformat__ = 'epytext'
import logging
from doapfiend.plugins.base import Plugin
from doapfiend.doaplib import fetch_doap, query_by_homepage
LOG = logging.getLogger('doapfiend')

class OutputPlugin(Plugin):
    """Class for formatting DOAP output"""
    name = 'homepage'
    enabled = False
    enable_opt = name

    def __init__(self):
        """Setup RDF/XML OutputPlugin class"""
        super(OutputPlugin, self).__init__()
        self.options = None
        return

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        search.add_option('-o', '--%s' % self.name, action='store', dest=self.enable_opt, help="Search for DOAP by a project's homepage", metavar='HOMEPAGE_URL')
        return (parser, output, search)

    def search(self):
        """
        Get DOAP given a project's homepage

        @rtype: unicode
        @return: DOAP
        """
        return do_search(self.options.homepage)


def do_search(homepage):
    """
    Get DOAP given a project's homepage

    @param homepage: Project homepage URL

    @rtype: unicode
    @return: DOAP
    """
    resp = query_by_homepage(homepage)
    LOG.debug(resp)
    if len(resp) == 0:
        LOG.error('Not found: %s' % homepage)
        return
    elif len(resp) == 1:
        url = resp[0][1]
    else:
        LOG.warn('Warning: Multiple DOAP found.')
        url = None
        for this in resp:
            LOG.warn(this)
            if not url:
                url = this[1]
            if this[0] == 'ex':
                url = this[1]

        LOG.warn('Using %s' % url)
    return fetch_doap(url)