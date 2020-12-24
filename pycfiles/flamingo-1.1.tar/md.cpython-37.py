# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/md.py
# Compiled at: 2020-03-20 06:59:09
# Size of source mod 2**32: 1225 bytes
from bs4 import BeautifulSoup
import markdown
from flamingo.core.utils.html import extract_title, process_media_links
from flamingo.core.parser import ContentParser

class MarkdownParser(ContentParser):
    FILE_EXTENSIONS = [
     'md']

    def parse(self, file_content, content):
        if not hasattr(self.context.settings, 'MARKDOWN_EXTENSIONS'):
            self.context.settings.MARKDOWN_EXTENSIONS = []
        if not hasattr(self.context.settings, 'MARKDOWN_EXTENSION_CONFIGS'):
            self.context.settings.MARKDOWN_EXTENSION_CONFIGS = {}
        md = self.parse_meta_data(file_content, content)
        extensions = self.context.settings.MARKDOWN_EXTENSIONS
        extension_configs = self.context.settings.MARKDOWN_EXTENSION_CONFIGS
        html = markdown.markdown(md, extensions=extensions, extension_configs=extension_configs)
        soup = BeautifulSoup(html, 'html.parser')
        title = extract_title(soup)
        process_media_links(self.context, content, soup)
        content['content_title'] = title
        content['content_body'] = str(soup)


class Markdown:

    def parser_setup(self, context):
        context.parser.add_parser(MarkdownParser(context))