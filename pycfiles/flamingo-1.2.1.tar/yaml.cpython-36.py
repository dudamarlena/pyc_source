# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/yaml.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 951 bytes
from flamingo.core.parser import ContentParser

class YamlParser(ContentParser):
    FILE_EXTENSIONS = [
     'yaml']

    def parse(self, file_content, content):
        file_content = file_content + '\n\n\n'
        self.parse_meta_data(file_content, content)


class Yaml:

    def parser_setup(self, context):
        context.parser.add_parser(YamlParser(context))