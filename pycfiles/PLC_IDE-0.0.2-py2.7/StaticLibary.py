# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\IDE\StaticLibary.py
# Compiled at: 2020-01-19 23:01:46
import sys
reload(sys)
sys.setdefaultencoding('utf8')
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def parse():
    tree = ET.ElementTree(file='Projects/test1/Helper/xml/____function_8h.xml')
    root = tree.getroot()
    for elem in tree.iterfind("./compounddef/sectiondef[@kind='func']/memberdef"):
        print elem.attrib['kind']
        print elem.findall('./definition')[0].text
        print elem.findall('./argsstring')[0].text
        print elem.findall('./name')[0].text