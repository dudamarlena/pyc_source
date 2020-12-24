# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dropstar/process.py
# Compiled at: 2010-10-14 14:04:21
"""
Process page rendering.
"""
import logging
from unidist.log import log
DEFAULT_PAGE_ARGS = ('redirect', )

def GetSiteConf(sites, host):
    """Get the site specified by the host in the conf."""
    default = None
    for (site, site_conf) in sites:
        if host == site:
            return site_conf
        elif default == None:
            default = site_conf

    return default


def RenderPage(site, page, conf, apps, data, state):
    """Render the page."""
    output = RenderOutput()
    run_input = {}
    run_input.update(state['headers'])
    run_input.update(state['cookies'])
    if state['session']:
        run_input.update(state['session'])
    run_input.update(data)
    log('Running script: %s  Path: %s' % (page, site['script_path_prefix']))
    run_output = runblock.RunScriptBlock(page, run_input, state, site['script_path_prefix'])
    template = GetTemplate(site, page, run_output)
    template_output = FormatTemplate(template, run_output)
    output += str(template_output)
    return output


def GetPage(path, site_conf):
    """Get the page information from the site_conf dict."""
    log('Get Path: "%s"  Site: %s' % (path, site_conf), logging.DEBUG)
    for (name, page) in site['page'].items():
        if path in page['aliases']:
            log('Page: %s' % page['title'], logging.DEBUG)
            return page

    return