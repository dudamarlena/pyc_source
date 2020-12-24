# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyupnptools/upnp_xml.py
# Compiled at: 2018-09-02 03:53:10
import xml.etree.ElementTree as ET, re
from . import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def read_xml(text):
    return ET.fromstring(text)


def get_namespace(node):
    return re.match('{(.+)}', node.tag).group(1)


def get_tagname(node):
    return node.tag.split('}')[(-1)]