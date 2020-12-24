# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/helloworld/helloworld.py
# Compiled at: 2011-08-19 13:49:32
"""
Created on Tue 16 Aug 2011

@author: leewei
"""
from trac.core import *
from trac.util.html import html
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor
import os, sys

class TixSummaryPlugin(Component):
    """
        Barebones Trac plugin to display a metanav link to ticket summary.
    """
    implements(INavigationContributor, IRequestHandler)

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        conf = self.env.config
        conf.set('header_logo', 'src', 'site/lshift-logo.png')
        conf.set('logging', 'log_level', 'DEBUG')
        conf.set('logging', 'log_type', 'file')
        conf.set('project', 'name', 'LShift')
        conf.set('project', 'url', 'http://www.lshift.net')
        conf.set('project', 'descr', 'Dev Trac instance')
        conf.set('trac', 'base_url', '/')
        conf.set('trac', 'debug_sql', 'yes')
        conf.set('traccron', 'ticker_enabled', True)
        conf.set('traccron', 'amqp_consumer.enabled', True)
        conf.set('traccron', 'amqp_consumer.cron', '0 0/1 * * * ?')
        conf.set('traccron', 'amqp_consumer.cron.enabled', True)
        conf.save()

    def get_active_navigation_item(self, req):
        return 'a-ticket-summary'

    def get_navigation_items(self, req):
        yield (
         'metanav', 'a-ticket-summary',
         html.A('Ticket Summary', href=req.href.tixsummary()))

    def match_request(self, req):
        return req.path_info == '/tixsummary'

    def process_request(self, req):
        return req.redirect(os.path.join(req.base_path, 'report/12'))