# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/customBurndownChart/tooltip.py
# Compiled at: 2011-09-19 06:45:14
"""
Created on Tue 16 Aug 2011

@author: leewei
"""
import os, re, urllib2
from config import *
from pkg_resources import resource_filename
from trac.core import *
from trac.web import IRequestHandler, IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script

class BurndownChartToolTip(Component):
    """
        Base class to provide minimal instructions as to how to fill out
        the 'estimatedtime' field, using jQuery UI/qTip2, in /newticket,
        /ticket/[0-9]+.
    """
    implements(IRequestHandler, IRequestFilter, ITemplateProvider)

    def match_request(self, req):
        """Return whether the handler wants to process the given request."""
        match = re.match('^/tooltip/(tooltip|qtip2).(css|js)$', req.path_info)
        if match and match.group(2):
            req.args['ext'] = match.group(2)
            return True
        return match or re.match('/jquery.*\\.js$', req.path_info)

    def process_request(self, req):
        """
            Process the request.

            Return a `(template_name, data, content_type)` tuple, where `data`
            is a dictionary of substitutions for the Genshi template.

            "text/html" is assumed if `content_type` is `None`.

            Note that if template processing should not occur, this method can
            simply send the response itself and not return anything.
        """
        if req.path_info == '/tooltip/tooltip.js':
            return ('tooltip.html', {}, 'text/javascript')
        if re.sub('tooltip/', '', req.path_info[1:]).startswith('qtip2'):
            if req.args['ext']:
                ext = req.args['ext']
                base_url = URL_CDN_QTIP2
                base_file = 'jquery.qtip'
                opener = urllib2.build_opener()
                if ext == 'css':
                    infile = opener.open(os.path.join(base_url, base_file + '.min.css'))
                    content = infile.read()
                    return (
                     'css.html', {'data': {'css': content}}, 'text/css')
                if ext == 'js':
                    infile = opener.open(os.path.join(base_url, base_file + '.min.js'))
                    content = infile.read()
                    return (
                     'js.html', {'data': {'js': content}}, 'text/javascript')
        elif re.match('/jquery.*\\.js$', req.path_info):
            cdn_js = URL_CDN_JQUERY
            opener = urllib2.build_opener()
            try:
                infile = opener.open(cdn_js)
            except URLError as msg:
                self.log.error('Unable to fetch jQuery JS from CDN: %s', msg)
                raise

            content = infile.read()
            return (
             'js.html', {'data': {'js': content}}, 'text/javascript')

    def pre_process_request(self, req, handler):
        """
            Called after initial handler selection, and can be used to change
            the selected handler or redirect request.

            Always returns the request handler, even if unchanged.
        """
        return handler

    def post_process_request(self, req, template, data, content_type):
        """
            Do any post-processing the request might need; typically adding
            values to the template `data` dictionary, or changing the Genshi
            template or mime type.

            `data` may be updated in place.

            Always returns a tuple of (template, data, content_type), even if
            unchanged.

            Note that `template`, `data`, `content_type` will be `None` if:
             - called when processing an error page
             - the default request handler did not return any result

            :Since 0.11: there's a `data` argument for supporting Genshi
               templates; this introduced a difference in arity which made it
               possible to distinguish between the IRequestFilter components
               still targeted at ClearSilver templates and the newer ones
               targeted at Genshi templates.
        """
        if req.path_info[1:].startswith(('ticket', 'newticket')):
            add_script(req, 'tooltip/js/jquery.js')
            add_stylesheet(req, '/tooltip/qtip2.css')
            add_script(req, '/tooltip/qtip2.js')
            add_script(req, '/tooltip/tooltip.js')
        return (
         template, data, content_type)

    def get_htdocs_dirs(self):
        """Return a list of directories with static resources (such as style
        sheets, images, etc.)

        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.

        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
        """
        return [
         (
          'tooltip', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """Return a list of directories containing the provided template
        files.
        """
        return [
         resource_filename(__name__, 'templates')]