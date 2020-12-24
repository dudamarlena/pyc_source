# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/html.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 948 bytes
from bs4 import BeautifulSoup
from flamingo.core.utils.html import extract_title, process_media_links
from flamingo.core.parser import ContentParser

class HTMLParser(ContentParser):
    FILE_EXTENSIONS = [
     'html']

    def parse(self, file_content, content):
        markup_string = self.parse_meta_data(file_content, content)
        soup = BeautifulSoup(markup_string, 'html.parser')
        raw_html = self.context.settings.HTML_PARSER_RAW_HTML or bool(content['raw_html'])
        if raw_html:
            content['content_title'] = ''
            content['content_body'] = markup_string
        else:
            title = extract_title(soup)
            process_media_links(self.context, content, soup)
            content['content_title'] = title
            content['content_body'] = str(soup)


class HTML:

    def parser_setup(self, context):
        context.parser.add_parser(HTMLParser(context))