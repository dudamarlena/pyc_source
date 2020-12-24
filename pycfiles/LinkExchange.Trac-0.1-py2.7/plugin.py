# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/trac/plugin.py
# Compiled at: 2011-05-12 17:23:14
import logging, re
from trac.core import *
from trac.web import IRequestFilter, ITemplateStreamFilter, IRequestHandler
from genshi import XML, ParseError
from genshi.output import XMLSerializer
from linkexchange.trac import support
from linkexchange.utils import rearrange_blocks, parse_rearrange_map
log = logging.getLogger('linkexchange.trac')

class LinkExchangePlugin(Component):
    implements(IRequestFilter)
    implements(ITemplateStreamFilter)
    implements(IRequestHandler)

    def __init__(self):
        super(LinkExchangePlugin, self).__init__(self)
        support.configure(self)
        self.lx_filter_template_match = re.compile(self.lx_options.get('filter_template_match', '^wiki_view\\.html$'))
        self.lx_filter_path_match = re.compile(self.lx_options.get('filter_path_match', '^.*'))
        if self.lx_options.get('handler_path_match', ''):
            self.lx_handler_path_match = re.compile(self.lx_options['handler_path_match'])
        else:
            self.lx_handler_path_match = None
        return

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if data is None:
            return (template, data, content_type)
        else:
            if self.lx_platform is None:
                return (template, data, content_type)
            lx_request = support.convert_request(req, self.lx_options)
            if self.lx_formatters:
                data['linkexchange_blocks'] = self.lx_platform.get_blocks(lx_request, self.lx_formatters)
                try:
                    rearrange_map = parse_rearrange_map(self.lx_options['rearrange_map'])
                except KeyError:
                    pass
                except ValueError:
                    log.warning('Unable to parse rearrange_map')
                else:
                    data['linkexchange_blocks'] = rearrange_blocks(lx_request, data['linkexchange_blocks'], rearrange_map)

            if self.lx_options.get('use_raw_links', False):
                data['linkexchange_links'] = self.lx_platform.get_raw_links(lx_request)
            return (template, data, content_type)

    def filter_stream(self, req, method, filename, stream, data):
        if method != 'xhtml':
            return stream
        else:
            if self.lx_platform is None:
                return stream
            if not self.lx_options.get('content_filtering', False):
                return stream
            if not self.lx_filter_template_match.match(filename):
                return stream
            if not self.lx_filter_path_match.match(req.path_info):
                return stream
            log.debug('Filtering event stream: method=%s; filename=%s', method, filename)
            content = ('').join(XMLSerializer()(stream))
            lx_request = support.convert_request(req, self.lx_options)
            new_content = self.lx_platform.content_filter(lx_request, content)
            try:
                stream = XML(new_content)
            except ParseError:
                log.error('Error parsing XML', exc_info=True)
                log.debug('Invalid XML data:\n%s', new_content)
                stream = XML(content)

            return stream

    def match_request(self, req):
        if self.lx_platform is None:
            return False
        else:
            if self.lx_handler_path_match is None:
                return False
            return self.lx_handler_path_match.match(req.path_info)

    def process_request(self, req):
        lx_request = support.convert_request(req, self.lx_options)
        lx_response = self.lx_platform.handle_request(lx_request)
        req.send_response(lx_response.status)
        headers = lx_response.headers.copy()
        headers.setdefault('Content-Length', str(len(lx_response.body)))
        for k, v in headers.items():
            req.send_header(k, v)

        req.end_headers()
        req.write(lx_response.body)