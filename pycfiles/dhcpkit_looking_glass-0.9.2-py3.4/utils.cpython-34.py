# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/utils.py
# Compiled at: 2016-07-18 18:22:20
# Size of source mod 2**32: 906 bytes
"""
Miscellaneous utilities for the looking glass
"""
import json, re
from collections import OrderedDict
import yaml
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from typing import Optional

def json_message_to_html(json_message: Optional[str]) -> Optional[str]:
    """
    Show a message (which is stored as JSON in the database) as YAML with some highlighting.

    :param json_message: The JSON string
    :return: The HTML representation
    """
    if not json_message:
        return
    response_yaml = yaml.dump(json.loads(json_message, object_pairs_hook=OrderedDict), default_flow_style=False)
    response_html = format_html('<pre style="float: left; margin: 0">{}</pre>', response_yaml)
    response_html = re.sub('([a-zA-Z0-9]+Message:)', '<b>\\1</b>', response_html)
    return mark_safe(response_html)