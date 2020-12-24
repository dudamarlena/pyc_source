# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/metadata.py
# Compiled at: 2019-05-16 13:41:33
import yaml
from insights.core import Parser
from insights.core.plugins import parser
from insights.specs import Specs

@parser(Specs.metadata_json)
class MetadataJson(Parser):

    def parse_content(self, content):
        self.data = yaml.safe_load(content)