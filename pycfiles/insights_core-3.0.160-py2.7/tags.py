# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tags.py
# Compiled at: 2019-11-14 13:58:37
from insights.core import JSONParser
from insights.core.plugins import parser
from insights.specs import Specs

@parser(Specs.tags)
class Tags(JSONParser):
    """ Class for parsing the content of ``tags.json``."""
    pass